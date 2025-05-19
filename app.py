# === Onglet 1 : Antibiotiques 2024 ===
with tab1:
    st.header("📌 Antibiotiques - Données 2024")
    uploaded_file = st.file_uploader("📁 Charger un fichier CSV ou Excel", type=["csv", "xlsx"], key="upload_ab")
    
    if uploaded_file:
        df_ab = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
        st.success(f"✅ Fichier chargé : {uploaded_file.name}")
    else:
        df_ab = pd.read_csv("tests_par_semaine_antibiotiques_2024.csv")
    
    df_ab.columns = df_ab.columns.str.strip()
    st.write("📋 Colonnes détectées :", df_ab.columns.tolist())

    # 🔍 Détection automatique de la colonne "Week"
    possible_names = ["Week", "Semaine", "week", "semaine"]
    week_col = next((col for col in df_ab.columns if col in possible_names), None)

    if not week_col:
        st.error("❌ Aucune colonne correspondant à 'Week' ou 'Semaine' trouvée.")
        st.stop()

    df_ab = df_ab[df_ab[week_col].apply(lambda x: str(x).isdigit())]
    df_ab[week_col] = df_ab[week_col].astype(int)
    ab_cols = [col for col in df_ab.columns if col.startswith('%')]

    if not ab_cols:
        st.warning("Aucune colonne de pourcentage détectée. Vérifiez le contenu du fichier.")
        st.stop()

    selected_ab = st.selectbox("Sélectionner un antibiotique", ab_cols, key="ab2024")
    week_range = st.slider("Plage de semaines", df_ab[week_col].min(), df_ab[week_col].max(), key="range_ab2024")
    df_filtered = df_ab[df_ab[week_col].between(*week_range)]

    values = pd.to_numeric(df_filtered[selected_ab], errors='coerce').dropna()
    q1, q3 = np.percentile(values, [25, 75])
    iqr, lower, upper = q3 - q1, max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=df_filtered[selected_ab], mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[upper]*len(df_filtered), line=dict(dash='dash'), name="Seuil haut"))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[lower]*len(df_filtered), line=dict(dash='dot'), name="Seuil bas"))
    fig.update_layout(xaxis_title="Semaine", yaxis_title="Résistance (%)")
    st.plotly_chart(fig, use_container_width=True)

    semaine_pic = df_filtered.loc[df_filtered[selected_ab].idxmax(), week_col]
    st.markdown("### 🧾 Résumé")
    st.write(f"📊 Moyenne : {df_filtered[selected_ab].mean():.2f} %")
    st.write(f"💥 Semaine pic : {semaine_pic}")
# === Onglet 2 : Autres Antibiotiques ===
with tab2:
    st.header("🧪 Autres Antibiotiques - Staph aureus")
    uploaded_file_other = st.file_uploader("📁 Charger un fichier pour Autres Antibiotiques", type=["csv", "xlsx"], key="upload_other")

    if uploaded_file_other:
        df_other = pd.read_csv(uploaded_file_other) if uploaded_file_other.name.endswith("csv") else pd.read_excel(uploaded_file_other)
        st.success(f"✅ Fichier chargé : {uploaded_file_other.name}")
    else:
        df_other = pd.read_excel("other Antibiotiques staph aureus.xlsx")

    df_other.columns = df_other.columns.str.strip()
    st.write("📋 Colonnes détectées :", df_other.columns.tolist())

    # 🔍 Détection automatique de la colonne "Week"
    possible_names = ["Week", "Semaine", "week", "semaine"]
    week_col = next((col for col in df_other.columns if col in possible_names), None)

    if not week_col:
        st.error("❌ Aucune colonne correspondant à 'Week' ou 'Semaine' trouvée.")
        st.stop()

    df_other = df_other[df_other[week_col].apply(lambda x: str(x).isdigit())]
    df_other[week_col] = df_other[week_col].astype(int)
    ab_cols = [col for col in df_other.columns if col.startswith('%')]

    if not ab_cols:
        st.warning("Aucune colonne de pourcentage détectée. Vérifiez le contenu du fichier.")
        st.stop()

    selected_ab = st.selectbox("Sélectionner un antibiotique", ab_cols, key="ab_other")
    week_range = st.slider("Plage de semaines", df_other[week_col].min(), df_other[week_col].max(), key="range_ab_other")
    df_filtered = df_other[df_other[week_col].between(*week_range)]

    values = pd.to_numeric(df_filtered[selected_ab], errors='coerce').dropna()
    q1, q3 = np.percentile(values, [25, 75])
    iqr, lower, upper = q3 - q1, max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=df_filtered[selected_ab], mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[upper]*len(df_filtered), line=dict(dash='dash'), name="Seuil haut"))
    fig.add_trace(go.Scatter(x=df_filtered[week_col], y=[lower]*len(df_filtered), line=dict(dash='dot'), name="Seuil bas"))
    fig.update_layout(xaxis_title="Semaine", yaxis_title="Résistance (%)")
    st.plotly_chart(fig, use_container_width=True)
# === Onglet 3 : Phénotypes - Staph aureus ===
with tab3:
    st.header("🧬 Phénotypes - Staph aureus")
    uploaded_file_pheno = st.file_uploader("📁 Charger un fichier de phénotypes", type=["xlsx"], key="upload_pheno")

    if uploaded_file_pheno:
        df_pheno = pd.read_excel(uploaded_file_pheno)
        st.success(f"✅ Fichier chargé : {uploaded_file_pheno.name}")
    else:
        df_pheno = pd.read_excel("staph_aureus_pheno_final.xlsx")

    # 🔍 Nettoyage et vérifications
    df_pheno.columns = df_pheno.columns.str.strip()
    st.write("📋 Colonnes détectées :", df_pheno.columns.tolist())

    if "week" not in df_pheno.columns:
        st.error("❌ Colonne 'week' non trouvée. Vérifiez le fichier.")
        st.stop()

    df_pheno["week"] = pd.to_datetime(df_pheno["week"], errors="coerce")
    df_pheno = df_pheno.dropna(subset=["week"])
    df_pheno["Week"] = df_pheno["week"].dt.date

    phenos = ["MRSA", "Other", "VRSA", "Wild"]
    missing = [p for p in phenos if p not in df_pheno.columns]
    if missing:
        st.error(f"❌ Colonnes manquantes : {missing}")
        st.stop()

    df_pheno["Total"] = df_pheno[phenos].sum(axis=1)
    for pheno in phenos:
        df_pheno[f"% {pheno}"] = (df_pheno[pheno] / df_pheno["Total"]) * 100

    selected_pheno = st.selectbox("Sélectionner un phénotype", phenos)
    week_range = st.slider("Plage de semaines", df_pheno["Week"].min(), df_pheno["Week"].max(), key="pheno_range")
    df_filtered = df_pheno[(df_pheno["Week"] >= week_range[0]) & (df_pheno["Week"] <= week_range[1])]
    values = df_filtered[f"% {selected_pheno}"].dropna()

    q1, q3 = np.percentile(values, [25, 75])
    iqr, lower, upper = q3 - q1, max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered["Week"], y=df_filtered[f"% {selected_pheno}"], mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df_filtered["Week"], y=[upper]*len(df_filtered), line=dict(dash='dash'), name="Seuil haut"))
    fig.add_trace(go.Scatter(x=df_filtered["Week"], y=[lower]*len(df_filtered), line=dict(dash='dot'), name="Seuil bas"))
    fig.update_layout(
        xaxis_title="Semaine",
        yaxis_title="Résistance (%)",
        yaxis=dict(range=[0, 100] if selected_pheno == "MRSA" else [0, 30])
    )
    st.plotly_chart(fig, use_container_width=True)
# === Onglet 4 : Fiches Bactéries ===
with tab4:
    st.header("🧫 Détail des bactéries à étudier")

    try:
        df_bact = pd.read_excel("TOUS les bacteries a etudier.xlsx")
        df_bact.columns = df_bact.columns.str.strip()
        st.write("📋 Colonnes détectées :", df_bact.columns.tolist())
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {e}")
        st.stop()

    if "Category" not in df_bact.columns or "Key Antibiotics" not in df_bact.columns:
        st.error("❌ Le fichier doit contenir au moins les colonnes 'Category' et 'Key Antibiotics'.")
        st.stop()

    search = st.text_input("🔍 Rechercher une bactérie :", "", key="search_bact")
    filtered_df = df_bact[df_bact["Category"].str.contains(search, case=False, na=False)]

    st.subheader("📋 Liste des bactéries")
    if filtered_df.empty:
        st.info("Aucune bactérie ne correspond à votre recherche.")
    else:
        st.dataframe(filtered_df[["Category", "Key Antibiotics"]])

        selected = st.selectbox("📌 Sélectionner une bactérie :", filtered_df["Category"].unique(), key="select_bact")
        details = df_bact[df_bact["Category"] == selected].iloc[0]

        st.markdown(f"## 🧬 Détails : {selected}")
        st.write("**🔑 Key Antibiotics**")
        st.write(details.get("Key Antibiotics", "Non disponible"))

        st.write("**💊 Other Antibiotics**")
        st.write(details.get("Other Antibiotics", "Non disponible"))

        st.write("**🧬 Phénotype**")
        st.write(details.get("Phenotype", "Non disponible"))
# === Onglet 5 : Alertes par service ===
with tab5:
    st.header("⚠️ Alertes par service")

    uploaded_file_service = st.file_uploader(
        "📁 Charger un fichier de services hebdomadaires (Excel)",
        type=["xlsx"], key="upload_service"
    )

    try:
        if uploaded_file_service:
            df_service = pd.read_excel(uploaded_file_service)
            st.success(f"✅ Fichier chargé : {uploaded_file_service.name}")
        else:
            df_service = pd.read_excel("staph aureus hebdomadaire excel.xlsx")
    except Exception as e:
        st.error(f"❌ Erreur de lecture du fichier : {e}")
        st.stop()

    df_service.columns = df_service.columns.str.strip()
    st.write("📋 Colonnes détectées :", df_service.columns.tolist())

    if "DATE_ENTREE" not in df_service.columns or "LIBELLE_DEMANDEUR" not in df_service.columns:
        st.error("❌ Le fichier doit contenir les colonnes 'DATE_ENTREE' et 'LIBELLE_DEMANDEUR'.")
        st.stop()

    df_service['DATE_ENTREE'] = pd.to_datetime(df_service['DATE_ENTREE'], errors='coerce')
    df_service = df_service.dropna(subset=['DATE_ENTREE'])

    df_service['Week'] = df_service['DATE_ENTREE'].dt.isocalendar().week

    unique_weeks = sorted(df_service['Week'].dropna().unique().astype(int))
    if not unique_weeks:
        st.info("Aucune semaine valide détectée dans les données.")
        st.stop()

    selected_week = st.selectbox("📆 Semaine à consulter :", unique_weeks)

    services_week = df_service[df_service['Week'] == selected_week]['LIBELLE_DEMANDEUR'].dropna().unique()
    
    if len(services_week) > 0:
        st.markdown(f"### 🏥 Services enregistrés en semaine {selected_week}")
        for s in services_week:
            st.write(f"🔸 {s}")
    else:
        st.info("Aucun service enregistré pour cette semaine.")
