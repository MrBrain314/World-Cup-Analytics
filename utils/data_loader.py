import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "world_cup_results.xlsx"

@st.cache_data
def load_matches():
    df = pd.read_excel(DATA_PATH, sheet_name="WorldCupMatches")
    df["TotalGoals"] = df["HomeGoals"] + df["AwayGoals"]
    df["Result"] = df.apply(
        lambda r: "Home Win" if r["HomeGoals"] > r["AwayGoals"]
        else ("Away Win" if r["HomeGoals"] < r["AwayGoals"] else "Draw"),
        axis=1,
    )
    return df

@st.cache_data
def load_cups():
    df = pd.read_excel(DATA_PATH, sheet_name="WorldCups")
    df["Attendance"] = pd.to_numeric(
        df["Attendance"].astype(str).str.replace(",", "."), errors="coerce"
    )
    return df

@st.cache_data
def load_team_view():
    return pd.read_excel(DATA_PATH, sheet_name="World Cup - Tableau format")
