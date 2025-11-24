import streamlit as st
from tensorflow.keras.models import load_model

# Config Page
st.set_page_config(
    page_title="Nutrimentum",
    page_icon="images/Nutrimentum.jpg",
    layout="centered"
)

# Header 
st.title("Nutrimentum: Your AI-Powered Indonesian Nutrition Companion")

st.markdown("""
Nutrimentum is a machine learning–based platform that helps Indonesians make healthier food choices in a simple and personalized way.

Just take a photo of your meal to instantly identify the dish and reveal detailed nutrition facts such as calories, protein, carbohydrates, and fat, all tailored for authentic Indonesian cuisine.

Whether you're aiming to lose weight, build muscle, boost your energy, or strengthen immunity, Nutrimentum gives you personalized food recommendations aligned with your health goals and taste preferences.
""")

# Main Features
st.header("Main Features")

## Nutri Guide
st.subheader("🥗 Nutri Guide")
st.markdown("""
Nutri Guide offers a personalized recommendation system to support your health goals through two smart approaches:

1. **Goal-Based Recommendation**  
   Get food suggestions that align with your primary health objective such as weight loss, muscle development, energy boost, heart health, or immunity support.

2. **Content-Based Filtering (Nutrient Similarity)**  
   Discover alternative foods with similar nutritional profiles to the ones you already eat — great for maintaining variety without sacrificing your goals.

**How to Use:**  
- Choose your primary health goal or a food you often eat.  
- Get a list of personalized food recommendations based on nutrients or lifestyle goals.
""")

## Snap Nutri
st.subheader("📸 Snap Nutri")
st.markdown("""
Snap Nutri lets you recognize your meal and instantly reveal its nutritional value using image classification. Trained on 23 popular Indonesian dishes, this feature is ideal for quick insights.

**How to Use:**  
1. Take a clear photo of your Indonesian meal.  
2. Upload the image in the app.  
3. View the dish name and its estimated nutritional content (calories, fat, protein, carbs, etc.).
""")

# Footer
st.markdown("---")
st.caption("Built by the Machine Learning Team using Streamlit | **Nutrimentum 2025**")


# # Model Klasifikasi
# @st.cache_resource
# def preload_model():
#     return load_model('models/classification_model.keras')

# if "classification_model" not in st.session_state:
#     with st.spinner("🔄 Memuat model klasifikasi..."):
#         st.session_state["classification_model"] = preload_model()