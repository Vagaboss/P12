import streamlit as st
import requests
import pandas as pd

# URL de ton API FastAPI
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Agritech Answers - Rendement agricole Testo",
    page_icon="🌾",
    layout="centered",
)

st.title("🌾 Agritech Answers Testo")
st.subheader("Outil d'aide à la décision pour les rendements agricoles")

st.markdown(
    """
Cette application permet :

- de **prédire le rendement** d'une culture donnée sur une parcelle ;
- de **recommander la meilleure culture** à implanter, en fonction des conditions agronomiques.

L'intelligence est dans l'API (FastAPI + modèle ML).  
Streamlit sert uniquement d’interface utilisateur.
"""
)

# ------------------ Choix du mode ------------------

mode = st.radio(
    "Choisissez le mode d'utilisation :",
    ("Prédiction", "Recommandation"),
    horizontal=True,
)

st.markdown("---")

# ------------------ Entrées communes (contexte parcelle) ------------------

st.header("📍 Contexte de la parcelle")

col1, col2 = st.columns(2)

with col1:
    region = st.selectbox("Région", ["North", "South", "East", "West"])
    soil_type = st.selectbox(
        "Type de sol",
        ["Sandy", "Clay", "Silt", "Loam", "Chalky", "Peaty"],
    )
    weather_condition = st.selectbox(
        "Condition météo",
        ["Sunny", "Cloudy", "Rainy"],
    )

with col2:
    rainfall_mm = st.slider("Pluviométrie annuelle (mm)", 0, 1200, 600, step=10)
    temperature_c = st.slider("Température moyenne (°C)", 0, 50, 25, step=1)
    days_to_harvest = st.slider("Jours jusqu'à la récolte", 60, 200, 120, step=5)

col3, col4 = st.columns(2)
with col3:
    fertilizer_used = st.checkbox("Engrais utilisé", value=True)
with col4:
    irrigation_used = st.checkbox("Irrigation utilisée", value=True)

# ------------------ MODE PRÉDICTION ------------------

if mode == "Prédiction":
    st.markdown("---")
    st.header("📈 Mode prédiction de rendement")

    crop = st.selectbox(
        "Culture",
        ["Barley", "Cotton", "Maize", "Rice", "Soybean", "Wheat"],
    )

    if st.button("Lancer la prédiction"):
        payload = {
            "Region": region,
            "Soil_Type": soil_type,
            "Crop": crop,
            "Rainfall_mm": float(rainfall_mm),
            "Temperature_Celsius": float(temperature_c),
            "Fertilizer_Used": bool(fertilizer_used),
            "Irrigation_Used": bool(irrigation_used),
            "Weather_Condition": weather_condition,
            "Days_to_Harvest": int(days_to_harvest),
        }

        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                predicted_yield = result["predicted_yield"]

                st.success(
                    f"✅ Rendement prédit pour **{crop}** : "
                    f"**{predicted_yield:.2f} tonnes/hectare**"
                )
                st.caption(
                    "Cette estimation est basée sur votre contexte de parcelle "
                    "(climat, sol, engrais, irrigation...)."
                )
            else:
                st.error(f"Erreur côté API : {response.status_code}\n{response.text}")
        except Exception as e:
            st.error(f"❌ Impossible de joindre l'API : {e}")

# ------------------ MODE RECOMMANDATION ------------------

else:
    st.markdown("---")
    st.header("🧠 Mode recommandation de culture")

    st.markdown(
        """
Dans ce mode, le modèle teste **toutes les cultures possibles** dans les mêmes
conditions de parcelle et renvoie un **classement des cultures** par rendement
prédit décroissant.
"""
    )

    if st.button("Obtenir les recommandations"):
        payload = {
            "Region": region,
            "Soil_Type": soil_type,
            "Rainfall_mm": float(rainfall_mm),
            "Temperature_Celsius": float(temperature_c),
            "Fertilizer_Used": bool(fertilizer_used),
            "Irrigation_Used": bool(irrigation_used),
            "Weather_Condition": weather_condition,
            "Days_to_Harvest": int(days_to_harvest),
        }

        try:
            response = requests.post(f"{API_URL}/recommend", json=payload)
            if response.status_code == 200:
                result = response.json()
                recs = result.get("recommendations", [])

                if not recs:
                    st.warning("Aucune recommandation retournée par l'API.")
                else:
                    df_recs = pd.DataFrame(recs)
                    df_recs = df_recs.sort_values(
                        by="predicted_yield", ascending=False
                    )

                    st.subheader("🌱 Classement des cultures recommandées")

                    # Graphique à barres
                    st.bar_chart(
                        data=df_recs.set_index("Crop")["predicted_yield"],
                        use_container_width=True,
                    )

                    # Tableau détaillé
                    st.subheader("📊 Détail des résultats")
                    st.dataframe(df_recs.reset_index(drop=True))

                    st.caption(
                        "Les cultures sont triées par rendement prédit décroissant. "
                        "L'objectif est d'aider l'agriculteur à choisir la culture "
                        "la plus performante compte tenu de ses conditions."
                    )
            else:
                st.error(f"Erreur côté API : {response.status_code}\n{response.text}")
        except Exception as e:
            st.error(f"❌ Impossible de joindre l'API : {e}")
