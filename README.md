import streamlit as st
import pandas as pd
import random
import time
from io import StringIO

# --- KONFIGURASI APLIKASI STREAMLIT ---
# Mengatur judul dan ikon halaman
st.set_page_config(
    page_title="Nutrimentum - Pendamping Nutrisi Indonesia Berbasis AI",
    page_icon="🥗",
    layout="wide"
)

# --- JUDUL UTAMA ---
st.title("🥗 Nutrimentum")
st.header("Pendamping Nutrisi Indonesia Berbasis AI Anda")

st.markdown("""
Nutrimentum membantu Anda membuat pilihan makanan yang lebih sehat dan personal.
Gunakan fitur **Snap Nutri** untuk mengenali makanan atau **Nutri Guide** untuk mendapatkan rekomendasi.
""")

# --- FUNGSI MOCK UNTUK MODEL (Tidak menggunakan ML/Model asli karena keterbatasan file) ---

# Data nutrisi tiruan untuk simulasi rekomendasi
MOCK_NUTRITION_DATA = {
    "Nasi Goreng": {"Kalori": 518, "Protein": 15, "Lemak": 22, "Karbo": 65},
    "Gado-Gado": {"Kalori": 300, "Protein": 12, "Lemak": 18, "Karbo": 25},
    "Sate Ayam (10 tusuk)": {"Kalori": 450, "Protein": 30, "Lemak": 25, "Karbo": 20},
    "Sayur Asem": {"Kalori": 100, "Protein": 5, "Lemak": 2, "Karbo": 18},
    "Soto Ayam": {"Kalori": 250, "Protein": 20, "Lemak": 10, "Karbo": 15},
    "Pecel Lele": {"Kalori": 550, "Protein": 35, "Lemak": 35, "Karbo": 20},
    "Bubur Ayam": {"Kalori": 380, "Protein": 18, "Lemak": 15, "Karbo": 45},
}

def classify_image(uploaded_file):
    """
    Fungsi tiruan untuk Image Classification (Snap Nutri).
    Dalam aplikasi nyata, ini akan memuat model InceptionV3 dan memproses gambar.
    """
    # Simulasi waktu pemrosesan
    time.sleep(1.5)
    
    # Memilih hasil klasifikasi tiruan
    dish_name = random.choice(list(MOCK_NUTRITION_DATA.keys()))
    nutrition = MOCK_NUTRITION_DATA[dish_name]
    
    return {
        "dish": dish_name,
        "nutrition": nutrition,
        "confidence": random.uniform(0.85, 0.99)
    }

def get_recommendations(goal, selected_food=None):
    """
    Fungsi tiruan untuk Sistem Rekomendasi (Nutri Guide).
    Dalam aplikasi nyata, ini akan menggunakan filtering berbasis aturan atau cosine similarity.
    """
    time.sleep(1.5)
    
    all_foods = list(MOCK_NUTRITION_DATA.keys())
    
    if goal == "Weight Loss (Defisit Kalori)":
        # Rekomendasi rendah kalori (Goal-Based)
        recs = [food for food, data in MOCK_NUTRITION_DATA.items() if data["Kalori"] < 350]
        rec_type = "Goal-Based (Rendah Kalori)"
    elif goal == "Muscle Development (Tinggi Protein)":
        # Rekomendasi tinggi protein (Goal-Based)
        recs = [food for food, data in MOCK_NUTRITION_DATA.items() if data["Protein"] > 18]
        rec_type = "Goal-Based (Tinggi Protein)"
    elif selected_food:
        # Simulasi Content-Based Filtering (Menemukan alternatif)
        recs = [f for f in all_foods if f != selected_food and f != "Nasi Goreng"]
        random.shuffle(recs)
        recs = recs[:3]
        rec_type = f"Content-Based (Mirip {selected_food})"
    else:
        recs = random.sample(all_foods, 3)
        rec_type = "General"

    if not recs:
        return ["Tidak ada rekomendasi yang ditemukan untuk kriteria ini."], "General"
    
    return recs[:3], rec_type

# --- INTERFACE TAB ---

tab1, tab2 = st.tabs(["📸 Snap Nutri (Klasifikasi Gambar)", "🍽️ Nutri Guide (Rekomendasi Personal)"])

with tab1:
    st.header("Snap Nutri")
    st.subheader("Kenali Makanan Anda dalam Sekejap")
    st.markdown("Unggah foto makanan khas Indonesia Anda untuk mengetahui namanya dan perkiraan nilai nutrisinya.")
    
    uploaded_file = st.file_uploader(
        "Pilih Gambar Makanan...", 
        type=["png", "jpg", "jpeg"]
    )
    
    if uploaded_file is not None:
        # Menampilkan gambar yang diunggah
        st.image(uploaded_file, caption='Gambar yang Diunggah.', use_column_width=True, width=300)
        
        with st.spinner('Menganalisis gambar menggunakan InceptionV3...'):
            result = classify_image(uploaded_file)
            
        st.success("Analisis Selesai!")
        
        col_dish, col_conf = st.columns([2, 1])
        with col_dish:
            st.metric(label="Nama Makanan yang Dikenali", value=result["dish"])
        with col_conf:
            st.metric(label="Tingkat Keyakinan", value=f'{result["confidence"]:.2f}%')
            
        st.subheader("Perkiraan Nilai Nutrisi (Per Porsi)")
        nutrition_df = pd.DataFrame(
            result["nutrition"], 
            index=["Nilai (gram/Kalori)"]
        ).T
        st.table(nutrition_df.style.format("{:.0f}"))

        st.info("Peringatan: Nilai nutrisi ini adalah perkiraan. Selalu konsultasikan dengan ahli gizi.")

with tab2:
    st.header("Nutri Guide")
    st.subheader("Rekomendasi Makanan Sesuai Tujuan Kesehatan Anda")

    rec_mode = st.radio(
        "Pilih Mode Rekomendasi:",
        ["Goal-Based Recommendation", "Content-Based Filtering"],
        horizontal=True,
        index=0
    )

    recommended_foods = []
    
    if rec_mode == "Goal-Based Recommendation":
        goal = st.selectbox(
            "Pilih Tujuan Kesehatan Utama Anda:",
            ["Weight Loss (Defisit Kalori)", "Muscle Development (Tinggi Protein)", "Energy Boost", "Heart Health", "Immunity Support"]
        )
        if st.button("Dapatkan Rekomendasi (Goal-Based)", type="primary"):
            with st.spinner(f'Mencari makanan untuk tujuan "{goal}"...'):
                recommended_foods, rec_type = get_recommendations(goal)
            st.success(f"Rekomendasi {rec_type} Ditemukan!")

    elif rec_mode == "Content-Based Filtering":
        food_list = list(MOCK_NUTRITION_DATA.keys())
        selected_food = st.selectbox(
            "Pilih Makanan yang Sering Anda Konsumsi (untuk mencari alternatif serupa):",
            food_list
        )
        st.markdown("_Sistem akan merekomendasikan makanan yang memiliki profil nutrisi serupa._")
        if st.button("Dapatkan Rekomendasi (Content-Based)", type="primary"):
            with st.spinner(f'Mencari alternatif nutrisi yang mirip dengan "{selected_food}"...'):
                recommended_foods, rec_type = get_recommendations(None, selected_food)
            st.success(f"Rekomendasi {rec_type} Ditemukan!")

    if recommended_foods:
        st.subheader("Hasil Rekomendasi")
        
        for i, food in enumerate(recommended_foods):
            data = MOCK_NUTRITION_DATA.get(food, {"Kalori": 0, "Protein": 0, "Lemak": 0, "Karbo": 0})
            st.markdown(f"#### {i+1}. {food}")
            st.markdown(f"""
                <div style="padding: 10px; border: 1px solid #ccc; border-radius: 8px; margin-bottom: 10px;">
                    **Kalori:** {data['Kalori']} kcal | 
                    **Protein:** {data['Protein']}g | 
                    **Lemak:** {data['Lemak']}g | 
                    **Karbo:** {data['Karbo']}g
                </div>
            """, unsafe_allow_html=True)
            
# --- BAGIAN BAWAH ---
st.markdown("---")
st.caption("Nutrimentum Dibuat oleh Tim:")
st.caption("Development: Nabilah Putri Sawindra, Laila Zahrotul Firdausil Jannah, Muhammad Arif | ML: Frederick Godiva, Christian Nathaniel, Rafael Simarmata")
