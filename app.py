import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧬 Tableau de bord unifié - Résistances bactériennes")

# === Onglets ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📌 Antibiotiques 2024", 
    "🧪 Autres Antibiotiques", 
    "🧠 Phénotypes Staph aureus", 
    "🧫 Fiches Bactéries",
    "🔔 Alertes par service"
])

# === Onglet 1 : Antibiotiques 2024 ===
with tab1:
    st.header("📌 Antibiotiques - Données 2024")
    df_ab = pd.read_csv("tests_par_semaine_antibiotiques_2024.csv")
    df_ab.columns = df_ab.columns.str.strip()

    week_col = "Week" if "Week" in df_ab.columns else df_ab.columns[0]
    df_ab = df_ab[df_ab[week_col].apply(lambda x: str(x).isdigit())]
    df_ab[week_col] = df_ab[week_col].astype(int)
    ab_cols = [col for col in df_ab.columns if col.startswith('%')]

    selected_ab = st.selectbox("Sélectionner un antibiotique", ab_cols, key="ab2024")
    min_week, max_week = df_ab[week_col].min(), df_ab[week_col].max()
    week_range = st.slider("Plage de semaines", min_week, max_week, (min_week, max_week), key="range_ab2024")

    df_filtered = df_ab[(df_ab[week_col] >= week_range[0]) & (df_ab[week_col] <= week_range[1])]
    values = pd.to_numeric(df_filtered[selected_ab], errors='coerce').dropna()
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    lower, upper = max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=df_filtered[selected_ab], mode='lines+markers', name=selected_ab))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[upper]*len(df_filtered), mode='lines', name="Seuil haut", line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[lower]*len(df_filtered), mode='lines', name="Seuil bas", line=dict(dash='dot')))
    fig.update_layout(yaxis=dict(range=[0, 30]), xaxis_title="Semaine", yaxis_title="Résistance (%)")
    st.plotly_chart(fig, use_container_width=True)

    nb_tests = df_filtered[selected_ab].count()
    moyenne = df_filtered[selected_ab].mean()
    semaine_pic = df_filtered.loc[df_filtered[selected_ab].idxmax(), week_col]

    st.markdown("### 🧾 Résumé")
    st.write(f"🔢 **Nombre de semaines analysées** : {nb_tests}")
    st.write(f"📊 **Moyenne de résistance** : {moyenne:.2f} %")
    st.write(f"🚨 **Semaine avec le pic de résistance** : Semaine {semaine_pic}")

    last_val = df_filtered[selected_ab].dropna().iloc[-1]
    if last_val > upper:
        st.error(f"🚨 Alerte : la résistance est élevée cette semaine ({last_val:.2f} %)")
    elif last_val < lower:
        st.warning(f"⚠️ Résistance anormalement basse cette semaine ({last_val:.2f} %)")
    else:
        st.success(f"✅ Résistance dans la norme cette semaine ({last_val:.2f} %)")
# === Onglet 2 : Autres Antibiotiques ===
with tab2:
    st.header("🧪 Autres Antibiotiques - Staph aureus")
    df_other = pd.read_excel("other Antibiotiques staph aureus.xlsx")
    df_other.columns = df_other.columns.str.strip()

    week_col = "Week" if "Week" in df_other.columns else df_other.columns[0]
    df_other = df_other[df_other[week_col].apply(lambda x: str(x).isdigit())]
    df_other[week_col] = df_other[week_col].astype(int)
    other_cols = [col for col in df_other.columns if col.startswith('%')]

    selected_ab = st.selectbox("Sélectionner un antibiotique", other_cols, key="other_ab")
    min_week, max_week = df_other[week_col].min(), df_other[week_col].max()
    week_range = st.slider("Plage de semaines", min_week, max_week, (min_week, max_week), key="range_other_ab")

    df_filtered = df_other[(df_other[week_col] >= week_range[0]) & (df_other[week_col] <= week_range[1])]
    values = pd.to_numeric(df_filtered[selected_ab], errors='coerce').dropna()
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    lower, upper = max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=df_filtered[selected_ab], mode='lines+markers', name=selected_ab))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[upper]*len(df_filtered), mode='lines', name="Seuil haut", line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[lower]*len(df_filtered), mode='lines', name="Seuil bas", line=dict(dash='dot')))
    fig.update_layout(yaxis=dict(range=[0, 30]), xaxis_title="Semaine", yaxis_title="Résistance (%)")
    st.plotly_chart(fig, use_container_width=True)

    nb_tests = df_filtered[selected_ab].count()
    moyenne = df_filtered[selected_ab].mean()
    semaine_pic = df_filtered.loc[df_filtered[selected_ab].idxmax(), week_col]

    st.markdown("### 🧾 Résumé")
    st.write(f"🔢 **Nombre de semaines analysées** : {nb_tests}")
    st.write(f"📊 **Moyenne de résistance** : {moyenne:.2f} %")
    st.write(f"🚨 **Semaine avec le pic de résistance** : Semaine {semaine_pic}")

    last_val = df_filtered[selected_ab].dropna().iloc[-1]
    if last_val > upper:
        st.error(f"🚨 Alerte : la résistance est élevée cette semaine ({last_val:.2f} %)")
    elif last_val < lower:
        st.warning(f"⚠️ Résistance anormalement basse cette semaine ({last_val:.2f} %)")
    else:
        st.success(f"✅ Résistance dans la norme cette semaine ({last_val:.2f} %)")

# === Onglet 3 : Phénotypes ===
with tab3:
    st.header("🧠 Phénotypes - Staphylococcus aureus")
    df_pheno = pd.read_excel("staph_aureus_pheno_final.xlsx")
    df_pheno.columns = df_pheno.columns.str.strip()
    df_pheno["week"] = pd.to_datetime(df_pheno["week"], errors="coerce")
    df_pheno = df_pheno.dropna(subset=["week"])
    df_pheno["Week"] = df_pheno["week"].dt.date
    phenos = ["MRSA", "Other", "VRSA", "Wild"]
    df_pheno["Total"] = df_pheno[phenos].sum(axis=1)
    for pheno in phenos:
        df_pheno[f"% {pheno}"] = (df_pheno[pheno] / df_pheno["Total"]) * 100

    selected_pheno = st.selectbox("Sélectionner un phénotype", phenos, key="pheno")
    min_date, max_date = df_pheno["Week"].min(), df_pheno["Week"].max()
    date_range = st.slider("Plage de semaines", min_date, max_date, (min_date, max_date), key="range_pheno")

    filtered_pheno = df_pheno[(df_pheno["Week"] >= date_range[0]) & (df_pheno["Week"] <= date_range[1])]
    pct_col = f"% {selected_pheno}"
    values = filtered_pheno[pct_col].dropna()
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    lower, upper = max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=filtered_pheno[pct_col],
                             mode='lines+markers', name=f"% {selected_pheno}"))
    fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=[upper]*len(filtered_pheno),
                             mode='lines', name="Seuil haut", line=dict(dash='dash', color='red')))
    fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=[lower]*len(filtered_pheno),
                             mode='lines', name="Seuil bas", line=dict(dash='dot', color='red')))
    fig.update_layout(yaxis=dict(range=[0, 100] if selected_pheno == "MRSA" else [0, 30]), xaxis_title="Semaine", yaxis_title="Résistance (%)")
    st.plotly_chart(fig, use_container_width=True)

    nb_tests = filtered_pheno[pct_col].count()
    moyenne = filtered_pheno[pct_col].mean()
    semaine_pic = filtered_pheno.loc[filtered_pheno[pct_col].idxmax(), "Week"]

    st.markdown("### 🧾 Résumé")
    st.write(f"🔢 **Nombre de semaines analysées** : {nb_tests}")
    st.write(f"📊 **Moyenne de {selected_pheno}** : {moyenne:.2f} %")
    st.write(f"🚨 **Semaine avec le pic de {selected_pheno}** : {semaine_pic}")

    last_val = filtered_pheno[pct_col].dropna().iloc[-1]
    if last_val > upper:
        st.error(f"🚨 Alerte : taux élevé de **{selected_pheno}** cette semaine ({last_val:.2f} %)")
    elif last_val < lower:
        st.warning(f"⚠️ Taux anormalement bas de **{selected_pheno}** cette semaine ({last_val:.2f} %)")
    else:
        st.success(f"✅ Taux de **{selected_pheno}** dans la norme cette semaine ({last_val:.2f} %)")
# === Onglet 4 : Fiches Bactéries ===
with tab4:
    st.header("🧫 Détail des bactéries à étudier")
    df_bact = pd.read_excel("TOUS les bacteries a etudier.xlsx")
    df_bact.columns = df_bact.columns.str.strip()

    search = st.text_input("🔍 Rechercher une bactérie :", "", key="search_bact")
    filtered_df = df_bact[df_bact["Category"].str.contains(search, case=False, na=False)]

    st.subheader("📋 Liste des bactéries")
    st.dataframe(filtered_df[["Category", "Key Antibiotics"]])

    if not filtered_df.empty:
        selected = st.selectbox("📌 Sélectionner une bactérie :", filtered_df["Category"].unique(), key="select_bact")
        details = df_bact[df_bact["Category"] == selected].iloc[0]
        st.markdown(f"## 🧬 Détails : {selected}")

        st.write("**🔑 Key Antibiotics**")
        st.write(details["Key Antibiotics"])

        st.write("**💊 Other Antibiotics**")
        st.write(details["Other Antibiotics"])

        st.write("**🧞 Phénotype**")
        st.write(details["Phenotype"])
    else:
        st.info("Aucune bactérie ne correspond à votre recherche.")

# === Onglet 5 : Alertes par service ===
with tab5:
    st.header("🔔 Services concernés par des alertes de résistance")

    df_service = pd.read_excel("staph aureus hebdomadaire excel.xlsx")
    df_service['DATE_ENTREE'] = pd.to_datetime(df_service['DATE_ENTREE'], errors='coerce')
    df_service = df_service.dropna(subset=['DATE_ENTREE'])
    df_service['Week'] = df_service['DATE_ENTREE'].dt.isocalendar().week
    df_service['Année'] = df_service['DATE_ENTREE'].dt.year
    df_service = df_service[df_service['Année'] == 2024]

    alert_weeks = []
    for df_path in ["tests_par_semaine_antibiotiques_2024.csv", "other Antibiotiques staph aureus.xlsx"]:
        df_tmp = pd.read_csv(df_path) if df_path.endswith(".csv") else pd.read_excel(df_path)
        df_tmp.columns = df_tmp.columns.str.strip()
        week_col = "Week" if "Week" in df_tmp.columns else df_tmp.columns[0]
        df_tmp = df_tmp[df_tmp[week_col].apply(lambda x: str(x).isdigit())]
        df_tmp[week_col] = df_tmp[week_col].astype(int)
        ab_cols = [col for col in df_tmp.columns if col.startswith('%')]
        for ab in ab_cols:
            values = pd.to_numeric(df_tmp[ab], errors='coerce').dropna()
            if not values.empty:
                q1, q3 = np.percentile(values, [25, 75])
                iqr = q3 - q1
                upper = q3 + 1.5 * iqr
                alert_subset = df_tmp[df_tmp[ab] > upper]
                alert_weeks += alert_subset[week_col].tolist()

    df_pheno = pd.read_excel("staph_aureus_pheno_final.xlsx")
    df_pheno['week'] = pd.to_datetime(df_pheno['week'], errors='coerce')
    df_pheno = df_pheno.dropna(subset=['week'])
    df_pheno['Week'] = df_pheno['week'].dt.isocalendar().week
    phenos = ["MRSA", "Other", "VRSA", "Wild"]
    df_pheno["Total"] = df_pheno[phenos].sum(axis=1)
    for pheno in phenos:
        df_pheno[f"% {pheno}"] = (df_pheno[pheno] / df_pheno["Total"]) * 100
        values = df_pheno[f"% {pheno}"].dropna()
        if not values.empty:
            q1, q3 = np.percentile(values, [25, 75])
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            alert_subset = df_pheno[df_pheno[f"% {pheno}"] > upper]
            alert_weeks += alert_subset["Week"].tolist()

    alert_weeks = sorted(set(int(w) for w in alert_weeks if pd.notna(w)))

    if alert_weeks:
        selected_week = st.selectbox("🗓️ Choisissez une semaine avec alerte :", alert_weeks)
        services_alertes = df_service[df_service["Week"] == selected_week]["DEMANDEUR"].dropna().unique()
        if len(services_alertes) > 0:
            selected_service = st.selectbox("🏥 Choisissez un service :", services_alertes)
            st.subheader(f"Données du service **{selected_service}** pour la semaine {selected_week}")
            df_details = df_service[(df_service["Week"] == selected_week) & (df_service["DEMANDEUR"] == selected_service)]
            st.dataframe(df_details)
        else:
            st.info("Aucun service enregistré pour cette semaine.")
    else:
        st.success("✅ Aucune semaine avec alerte détectée.")
