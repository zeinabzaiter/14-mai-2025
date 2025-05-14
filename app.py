import streamlit as st
import pandas as pd

# Charger les données
df = pd.read_excel("TOUS les bacteries a etudier.xlsx")

# Titre du dashboard
st.title("Dashboard des Bactéries à Étudier")

# Barre de recherche
search = st.text_input("🔍 Rechercher une bactérie :", "")

# Filtrage dynamique
filtered_df = df[df["Category"].str.contains(search, case=False, na=False)]

# Affichage du tableau filtré
st.subheader("📋 Liste des bactéries")
st.dataframe(filtered_df[["Category", "Key Antibiotics"]])

# Sélection pour détails
selected = st.selectbox("📌 Sélectionner une bactérie :", filtered_df["Category"].unique())

# Affichage des détails
details = df[df["Category"] == selected].iloc[0]
st.markdown(f"## 🧫 Détails : {selected}")

st.write("**🔑 Key Antibiotics**")
st.write(details["Key Antibiotics"])

st.write("**💊 Other Antibiotics**")
st.write(details["Other Antibiotics"])

st.write("**🧬 Phénotype**")
st.write(details["Phenotype"])
