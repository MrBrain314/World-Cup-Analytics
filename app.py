import streamlit as st
from pathlib import Path
from utils.style import inject_css, sidebar_setup

st.set_page_config(
    page_title="FIFA World Cup Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
sidebar_setup(Path(__file__).parent)

st.title("⚽ FIFA World Cup Analytics")
st.subheader("Exploration historique 1930 - 2014 & Prédiction 2026")

st.markdown("""
Bienvenue dans ce dashboard interactif dédié à la **Coupe du Monde de la FIFA**.

Utilisez le menu de gauche pour naviguer entre les sections :

| Page | Contenu |
|------|---------|
| 📊 **Overview** | KPIs globaux et timeline des éditions |
| 🌍 **Nations** | Domination historique par pays |
| 📈 **Évolution** | Tendances offensives et défensives |
| 🏆 **Records** | Scores extrêmes, anomalies et underdog stories |
| 🤖 **Prédiction 2026** | Modèle ML pour le vainqueur 2026 |
| 🏆 **Coupe du Monde 2026** | Annonce du tournoi : groupes, favoris et confédérations |

---
*Données : FIFA World Cup 1930 - 2014 • #DaCoTChallengeData*
""")
