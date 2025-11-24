import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

# Config Page
st.set_page_config(
    page_title="Nutrimentum",
    page_icon="images/Nutrimentum.jpg",
    layout="centered"
)

# Load model dan data
df_goals = joblib.load("models/df_goals.joblib")
scaler_goals = joblib.load("models/scaler_goals.joblib")
scaler_nutrients = joblib.load("models/scaler_nutrients.joblib")
sim_nutrients_df = joblib.load("models/cosine_sim_nutrients_df.joblib")

# const
goal_cols = ['weight_management', 'muscle_development', 'energy_boost', 'heart_health', 'immunity_strength']
goals_list = ["Weight Management", "Muscle Development", "Energy Boost", "Heart Health", "Immunity Strength"]

# Fungsi rekomendasi berdasarkan goal

def recipe_recommendations_based_goals(userGoals, items, k=15):
    userGoals_scaled = scaler_goals.transform([userGoals])
    df_user = pd.DataFrame(userGoals_scaled, columns=goal_cols)
    df_user["item"] = "userGoals"

    df_temp = pd.concat([items, df_user], ignore_index=True)
    cosine_sim = cosine_similarity(df_temp.drop(columns=["item"]))
    sim_df = pd.DataFrame(cosine_sim, index=df_temp["item"], columns=df_temp["item"])

    sim_scores = sim_df.loc["userGoals"].drop("userGoals").sort_values(ascending=False).head(k)
    result = sim_scores.reset_index().rename(columns={"index": "item", "userGoals": "similarity_score"})
    return result

# NutriGuide
st.title("NutriGuide: Smart Food Recommendations for Your Health & Nutrition")
st.markdown("""
Discover meals that align with your health goals or nutritional needs.  
Choose a focus area or a base dish, and let us recommend the best options tailored to you.
""")

# Recommendation Method
jenis_rekomendasi = st.radio("Choose your recommendation mode:", [
    "Based on Health Goals",
    "Based on Nutrient Similarity"
])

if "rekomendasi_index" not in st.session_state:
    st.session_state.rekomendasi_index = None
if "rekomendasi_df" not in st.session_state:
    st.session_state.rekomendasi_df = None

# Based on Goals
if jenis_rekomendasi == "Based on Health Goals":
    selected = st.selectbox("🎯 Select your primary health focus:", goals_list)
    user_goals = [0]*5
    user_goals[goals_list.index(selected)] = 10

    if st.button("🔍 Get Personalized Recommendations"):
        st.session_state.rekomendasi_df = recipe_recommendations_based_goals(user_goals, df_goals, k=20)
        st.session_state.rekomendasi_index = 0

# Based on Nutrition
else:
    makanan_dipilih = st.selectbox("🍲 Select a food item to find similar alternatives:", sim_nutrients_df.index.tolist())
    if st.button("🔍 Find Similar Foods"):
        hasil = sim_nutrients_df[makanan_dipilih].sort_values(ascending=False).drop(makanan_dipilih).head(20)
        st.session_state.rekomendasi_df = hasil.reset_index().rename(columns={makanan_dipilih: "similarity_score", "index": "item"})
        st.session_state.rekomendasi_index = 0

# Show Recommendation
if st.session_state.rekomendasi_df is not None and st.session_state.rekomendasi_index is not None:
    start = st.session_state.rekomendasi_index
    end = start + 4
    subset = st.session_state.rekomendasi_df.iloc[start:end]

    cols = st.columns(2)
    for idx, (_, row) in enumerate(subset.iterrows()):
        with cols[idx % 2]:
            st.markdown(f"### {row['item']}")

            base_name = row['item']
            jpg_path = f"images/{base_name}.jpg"
            jpeg_path = f"images/{base_name}.jpeg"

            if os.path.exists(jpg_path):
                image_path = jpg_path
            elif os.path.exists(jpeg_path):
                image_path = jpeg_path
            else:
                image_path = f"images/No Image.jpeg"

            st.image(image_path, use_container_width=True)

    if st.button("🔁 Show More Suggestions"):
        st.session_state.rekomendasi_index += 4
        if st.session_state.rekomendasi_index >= len(st.session_state.rekomendasi_df):
            st.session_state.rekomendasi_index = 0
        st.rerun()

# Footer
st.markdown("---")
st.caption("Built by the Machine Learning Team using Streamlit | **Nutrimentum 2025**")