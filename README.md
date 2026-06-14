# ⚽ FIFA World Cup Analytics & Prédiction 2026

Dashboard interactif d'analyse de l'histoire de la Coupe du Monde de la FIFA (1930-2014)
et de prédiction pour l'édition 2026, réalisé avec **Streamlit**, **Plotly** et **scikit-learn**.

> Projet réalisé dans le cadre du **#DaCoTChallengeData** (Data Community Togo · Togo AI Lab).

## 📊 Fonctionnalités

- **Overview** : KPIs globaux, carte mondiale des titres, timeline des éditions
- **Nations** : domination historique, Europe vs Amérique du Sud, analyse par équipe
- **Évolution** : tendances offensives, buts par format de tournoi
- **Records** : matchs prolifiques, plus grosses victoires, anomalies
- **Prédiction 2026** : modèle Random Forest entraîné sur l'historique
- **Coupe du Monde 2026** : annonce du tournoi, les 12 groupes, favoris et confédérations

## 🚀 Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

## 🗂️ Structure

```
World_Cup/
├── app.py                  # Page d'accueil
├── pages/                  # Les 6 pages du dashboard
├── utils/                  # Chargement données, modèle ML, style
├── data/                   # Jeu de données + tirage 2026
├── assets/                 # Logo
└── requirements.txt
```

## 🧠 Méthodologie du modèle

Le classement des favoris repose sur un **Random Forest** entraîné sur les performances
historiques par équipe (taux de victoire, buts marqués/encaissés, titres, podiums).
Les probabilités sont normalisées pour se cumuler à 100 %.

> ⚠️ Le modèle s'appuie uniquement sur les données **1930-2014** : il reflète la domination
> passée, pas la forme actuelle des équipes.

---

**Démo en ligne :** [World Cup Analytics](https://world-cup-analytics.streamlit.app/)

---

**Auteur** : OURO-TAGBA Bastou · Data Analyst
