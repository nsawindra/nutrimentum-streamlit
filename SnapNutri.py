import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.models import load_model
import tempfile
import requests
import os

# Page Configuration
st.set_page_config(
    page_title="Nutrimentum",
    page_icon="images/Nutrimentum.jpg",
    layout="centered"
)

# Load model from session_state
MODEL_URL = "https://huggingface.co/cnginn/indonesiafoodimageclassification/resolve/main/classification_model.keras"
MODEL_PATH = "classification_model.keras"

def download_model():
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)
        
@st.cache_resource
def load_keras_model():
    if not os.path.exists(MODEL_PATH):
        download_model()
    return tf.keras.models.load_model(MODEL_PATH)

# Load model with spinner
with st.spinner("🔄 Loading model, please wait..."):
    try:
        model = load_keras_model()
    except Exception as e:
        st.error(f"❗ Failed to load model: {e}")
        st.stop()


# Load Nutrition Data
@st.cache_data
def load_nutrition_data():
    df = pd.read_csv('datasets/nutrition_food.csv')
    df.columns = df.columns.str.strip().str.lower()
    df['item'] = df['item']
    return df

nutrition_df = load_nutrition_data()

# Class Labels
class_labels = [
    'ayam_bakar', 'ayam_goreng', 'ayam_semur', 'bakso', 'bubur', 'cumi_goreng', 'gado_gado',
    'gulai_ikan', 'iga_bakar', 'ikan_goreng', 'martabak_telur', 'mie_goreng', 'nasi_goreng',
    'nasi_tumpeng', 'nasi_uduk', 'opor_ayam', 'rawon', 'rendang', 'sate', 'sop_buntut',
    'soto', 'telur_dadar', 'telur_rebus'
]

# Function for Nutrition Fact
def render_nutrition_facts(nutr_table):
    rows_html = ""
    for key, value in nutr_table.items():
        rows_html += f"""
        <div class="nf-row">
            <span class="nf-key">{key}</span>
            <span class="nf-value">{value}</span>
        </div>
        """
    st.markdown(
        f"""
        <style>
        .nutrition-facts {{
            width: 100%;
            border: 3px solid black;
            padding: 16px;
            font-family: Arial, sans-serif;
            background-color: white;
            color: black;
            margin-top: 10px;
            border-radius: 8px;
        }}
        .nf-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 4px solid black;
            margin-bottom: 12px;
        }}
        .nf-header h2 {{
            font-size: 24px;
            margin: 0;
        }}
        .nf-header .nf-serving {{
            font-size: 14px;
            font-style: italic;
        }}
        .nf-row {{
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #000;
            padding: 6px 0;
            font-size: 15px;
        }}
        .nf-key {{
            font-weight: bold;
        }}
        .nf-value {{
            font-weight: normal;
        }}
        </style>
        <div class="nutrition-facts">
            <div class="nf-header">
                <h2>Nutrition Facts</h2>
                <div class="nf-serving">Per 100g Serving</div>
            </div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True
    )



# Snap Nutri
st.title("SnapNutri: Food Image Classification")
st.markdown("""
Upload a photo of an Indonesian dish, and our deep learning model will identify the food and reveal its nutritional information.
""")

uploaded_file = st.file_uploader("Upload an image (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        st.info("🔍 Processing image...")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        image = load_img(tmp_path, target_size=(299, 299))
        img_array = img_to_array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions)
        predicted_label = class_labels[predicted_index]
        confidence = predictions[0][predicted_index]

        readable_label = predicted_label.replace('_', ' ').title()

        # Show image
        st.image(image, caption="Uploaded Image", use_container_width=False)

        st.markdown(f"""
            <div style='font-size:26px; font-weight:bold; margin-bottom:4px;'>
                Prediction Result: {readable_label}
            </div>
        """, unsafe_allow_html=True)

        # Confidence 
        st.markdown(
            f"""
            <div style='margin-top: -10px; font-size: 18px;'>
                🔎 <b>Confidence:</b> {confidence * 100:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

    
        # Nutrisi Makanan
        manual_map = {
            "Sate": "Sate Ayam",
            "Bubur": "Bubur Ayam",
            "Soto": "Soto Ayam",
            "Ikan Goreng": "Ikan Bakar",
            "Bakso": "Bakso Ayam"
        }
        nutr_item_name = manual_map.get(readable_label, readable_label)
        nutrition_row = nutrition_df[nutrition_df['item'] == nutr_item_name]
        if not nutrition_row.empty:
            row = nutrition_row.iloc[0]

            # Flavor
            st.markdown(f"""
                <div style='font-size:14px; font-style:italic; margin-bottom:12px;'>
                    Flavor profile: {row['flavor_profile']}
                </div>
            """, unsafe_allow_html=True)

            # Nutrition Facts 
            render_nutrition_facts({
                "Calories (kcal)": row['kalori'],
                "Protein (g)": row['protein'],
                "Fat (g)": row['lemak'],
                "Carbohydrates (g)": row['karbohidrat'],
                "Fiber (g)": row['fiber_g'],
                "Sugars (g)": row['sugars_g'],
                "Saturated Fat (g)": row['saturated_fat_g'],
                "Cholesterol (g)": row['cholesterol_g'],
                "Sodium (mg)": row['sodium_mg'],
                "Iron (mg)": row['iron_mg'],
                "Zinc (mg)": row['zinc_mg'],
                "Calcium (mg)": row['calcium_mg'],
                "Vitamin B12 (mcg)": row['vitamin_b12_mcg'],
                "Vitamin A (mcg)": row['vitamin_a_mcg'],
                "Vitamin B (mcg)": row['vitamin_b_mcg'],
                "Vitamin C (mcg)": row['vitamin_c_mcg'],
                "Vitamin D (mcg)": row['vitamin_d_mcg'],
                "Vitamin E (mcg)": row['vitamin_e_mcg']
            })
        else:
            st.warning(f"❗ Nutrition data for **{readable_label}** not found.")

        with st.expander("🎯 Health Goal Match"):
            health_goals = {
                "Weight Management": row['weight_management'],
                "Muscle Development": row['muscle_development'],
                "Energy Boost": row['energy_boost'],
                "Heart Health": row['heart_health'],
                "Immunity Strength": row['immunity_strength'],
            }

            sorted_goals = sorted(
                [(goal, val) for goal, val in health_goals.items() if pd.notna(val) and str(val).strip() != ""],
                key=lambda x: float(x[1]) if str(x[1]).replace(".", "", 1).isdigit() else 0,
                reverse=True
            )

            for goal, val in sorted_goals:
                st.markdown(f"- **{goal}**: {val}")

            for goal, val in health_goals.items():
                if pd.isna(val) or str(val).strip() == "":
                    st.markdown(f"- **{goal}**: No data available")

    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")

# Footer
st.markdown("---")
st.caption("Built by the Machine Learning Team using Streamlit | **Nutrimentum 2025**")
