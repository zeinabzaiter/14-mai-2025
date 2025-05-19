import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
st.set_page_config(page_title="Tableau de bord unifié", layout="wide")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Antibiotiques 2024",
    "Autres Antibiotiques",
    "Phénotypes Staph aureus",
    "Fiches Bactéries",
    "Alertes par service"
])

with tab1:
    st.header("📌 Antibiotiques 2024")

# === Onglet 1 : Antibiotiques 2024 ===
with tab1:
    st.header("📌 Antibiotiques - Données 2024")
    uploaded_file_ab = st.file_uploader("📂 Charger un fichier CSV ou Excel", type=["csv", "xlsx"], key="upload_ab")

    if uploaded_file_ab is not None:
        try:
            if uploaded_file_ab.name.endswith(".csv"):
                df_ab = pd.read_csv(uploaded_file_ab)
            else:
                df_ab = pd.read_excel(uploaded_file_ab)

            df_ab.columns = df_ab.columns.str.strip()

            if "Week" in df_ab.columns:
                week_col = "Week"
            else:
                st.error("❌ Colonne 'Week' introuvable dans le fichier importé.")
                st.write("Colonnes trouvées :", list(df_ab.columns))
                st.stop()

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
            st.write(f"💥 **Semaine avec le pic de résistance** : Semaine {semaine_pic}")

            try:
                df_service = pd.read_excel("staph aureus hebdomadaire excel.xlsx")
                df_service['DATE_ENTREE'] = pd.to_datetime(df_service['DATE_ENTREE'], errors='coerce')
                df_service['Week'] = df_service['DATE_ENTREE'].dt.isocalendar().week
                services_pic = df_service[df_service['Week'] == semaine_pic]['LIBELLE_DEMANDEUR'].dropna().unique()
                if len(services_pic) > 0:
                    st.markdown(f"### 🏥 **Services présents la semaine du pic (S{semaine_pic}) :**")
                    for s in services_pic:
                        st.write(f"🔹 {s}")
                else:
                    st.info("Aucun service enregistré cette semaine-là.")
            except:
                st.warning("⚠️ Impossible d'afficher les services de la semaine du pic.")

            last_val = df_filtered[selected_ab].dropna().iloc[-1]
            if last_val > upper:
                st.error(f"🚨 Alerte : la résistance est élevée cette semaine ({last_val:.2f} %)")
                try:
                    semaine_actuelle = df_filtered[week_col].iloc[-1]
                    services = df_service[df_service['Week'] == semaine_actuelle]['LIBELLE_DEMANDEUR'].dropna().unique()
                    if len(services) > 0:
                        st.markdown("### 🏥 **Services concernés cette semaine :**")
                        for s in services:
                            st.write(f"🔸 {s}")
                    else:
                        st.info("Aucun service enregistré cette semaine.")
                except:
                    st.warning("⚠️ Impossible d'afficher les services concernés.")
            elif last_val < lower:
                st.warning(f"⚠️ Résistance anormalement basse cette semaine ({last_val:.2f} %)")
            else:
                st.success(f"✅ Résistance dans la norme cette semaine ({last_val:.2f} %)")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les données.")


# === Onglet 2 : Autres Antibiotiques ===
with tab2:
    st.header("🧪 Autres Antibiotiques - Staph aureus")
    uploaded_file_other = st.file_uploader("📂 Charger un fichier pour Autres Antibiotiques", type=["csv", "xlsx"], key="upload_other")

    if uploaded_file_other is not None:
        try:
            if uploaded_file_other.name.endswith(".csv"):
                df_other = pd.read_csv(uploaded_file_other)
            else:
                df_other = pd.read_excel(uploaded_file_other)

            df_other.columns = df_other.columns.str.strip()

            if "Week" in df_other.columns:
                week_col = "Week"
            else:
                st.error("❌ Colonne 'Week' introuvable dans le fichier importé.")
                st.write("Colonnes trouvées :", list(df_other.columns))
                st.stop()

            df_other = df_other[df_other[week_col].apply(lambda x: str(x).isdigit())]
            df_other[week_col] = df_other[week_col].astype(int)
            ab_cols = [col for col in df_other.columns if col.startswith('%')]

            selected_ab = st.selectbox("Sélectionner un antibiotique", ab_cols, key="ab_other")
            min_week, max_week = df_other[week_col].min(), df_other[week_col].max()
            week_range = st.slider("Plage de semaines", min_week, max_week, (min_week, max_week), key="range_ab_other")

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
            st.write(f"💥 **Semaine avec le pic de résistance** : Semaine {semaine_pic}")

            try:
                df_service = pd.read_excel("staph aureus hebdomadaire excel.xlsx")
                df_service['DATE_ENTREE'] = pd.to_datetime(df_service['DATE_ENTREE'], errors='coerce')
                df_service['Week'] = df_service['DATE_ENTREE'].dt.isocalendar().week
                services_pic = df_service[df_service['Week'] == semaine_pic]['LIBELLE_DEMANDEUR'].dropna().unique()
                if len(services_pic) > 0:
                    st.markdown(f"### 🏥 **Services présents la semaine du pic (S{semaine_pic}) :**")
                    for s in services_pic:
                        st.write(f"🔹 {s}")
                else:
                    st.info("Aucun service enregistré cette semaine-là.")
            except:
                st.warning("⚠️ Impossible d'afficher les services de la semaine du pic.")

            last_val = df_filtered[selected_ab].dropna().iloc[-1]
            if last_val > upper:
                st.error(f"🚨 Alerte : la résistance est élevée cette semaine ({last_val:.2f} %)")
                try:
                    semaine_actuelle = df_filtered[week_col].iloc[-1]
                    services = df_service[df_service['Week'] == semaine_actuelle]['LIBELLE_DEMANDEUR'].dropna().unique()
                    if len(services) > 0:
                        st.markdown("### 🏥 **Services concernés cette semaine :**")
                        for s in services:
                            st.write(f"🔸 {s}")
                    else:
                        st.info("Aucun service enregistré cette semaine.")
                except:
                    st.warning("⚠️ Impossible d'afficher les services concernés.")
            elif last_val < lower:
                st.warning(f"⚠️ Résistance anormalement basse cette semaine ({last_val:.2f} %)")
            else:
                st.success(f"✅ Résistance dans la norme cette semaine ({last_val:.2f} %)")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les données.")
# === Onglet 3 : Phénotypes Staph aureus ===
with tab3:
    st.header("🧬 Phénotypes - Staph aureus")
    uploaded_file_pheno = st.file_uploader("📂 Charger un fichier pour Phénotypes", type=["csv", "xlsx"], key="upload_pheno")

    if uploaded_file_pheno is not None:
        try:
            if uploaded_file_pheno.name.endswith(".csv"):
                df_pheno = pd.read_csv(uploaded_file_pheno)
            else:
                df_pheno = pd.read_excel(uploaded_file_pheno)

            df_pheno.columns = df_pheno.columns.str.strip()

            df_pheno["week"] = pd.to_datetime(df_pheno["week"], errors="coerce")
            df_pheno = df_pheno.dropna(subset=["week"])
            df_pheno["Week"] = df_pheno["week"].dt.date

            phenos = ["MRSA", "Other", "VRSA", "Wild"]
            df_pheno["Total"] = df_pheno[phenos].sum(axis=1)
            for pheno in phenos:
                df_pheno[f"% {pheno}"] = (df_pheno[pheno] / df_pheno["Total"]) * 100

            selected_pheno = st.selectbox("Sélectionner un phénotype", phenos)
            min_date, max_date = df_pheno["Week"].min(), df_pheno["Week"].max()
            date_range = st.slider("Plage de semaines", min_date, max_date, (min_date, max_date))

            filtered_pheno = df_pheno[(df_pheno["Week"] >= date_range[0]) & (df_pheno["Week"] <= date_range[1])]
            pct_col = f"% {selected_pheno}"
            values = filtered_pheno[pct_col].dropna()
            q1, q3 = np.percentile(values, [25, 75])
            iqr = q3 - q1
            lower, upper = max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=filtered_pheno[pct_col],
                                     mode='lines+markers', name=pct_col))
            fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=[upper]*len(filtered_pheno),
                                     mode='lines', name="Seuil haut", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=[lower]*len(filtered_pheno),
                                     mode='lines', name="Seuil bas", line=dict(dash='dot')))
            fig.update_layout(yaxis=dict(range=[0, 100]), xaxis_title="Semaine", yaxis_title="Résistance (%)")
            st.plotly_chart(fig, use_container_width=True)

            nb_tests = filtered_pheno[pct_col].count()
            moyenne = filtered_pheno[pct_col].mean()
            semaine_pic = filtered_pheno.loc[filtered_pheno[pct_col].idxmax(), "Week"]

            st.markdown("### 🧾 Résumé")
            st.write(f"🔢 **Nombre de semaines analysées** : {nb_tests}")
            st.write(f"📊 **Moyenne de {selected_pheno}** : {moyenne:.2f} %")
            st.write(f"💥 **Semaine avec le pic de {selected_pheno}** : {semaine_pic}")

            last_val = filtered_pheno[pct_col].dropna().iloc[-1]
            if last_val > upper:
                st.error(f"🚨 Alerte : taux élevé de {selected_pheno} cette semaine ({last_val:.2f} %)")
            elif last_val < lower:
                st.warning(f"⚠️ Taux anormalement bas de {selected_pheno} cette semaine ({last_val:.2f} %)")
            else:
                st.success(f"✅ Taux de {selected_pheno} dans la norme cette semaine ({last_val:.2f} %)")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les données.")


# === Onglet 4 : Fiches Bactéries ===
with tab4:
    st.header("🧫 Détail des bactéries à étudier")
    uploaded_file_bact = st.file_uploader("📂 Charger un fichier de bactéries à étudier", type=["xlsx"], key="upload_bact")

    if uploaded_file_bact is not None:
        try:
            df_bact = pd.read_excel(uploaded_file_bact)
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

                st.write("**🧬 Phénotype**")
                st.write(details["Phenotype"])
            else:
                st.info("Aucune bactérie ne correspond à votre recherche.")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les données.")
# === Onglet 3 : Phénotypes Staph aureus ===
with tab3:
    st.header("🧬 Phénotypes - Staph aureus")
    uploaded_file_pheno = st.file_uploader("📂 Charger un fichier pour Phénotypes", type=["csv", "xlsx"], key="upload_pheno")

    if uploaded_file_pheno is not None:
        try:
            if uploaded_file_pheno.name.endswith(".csv"):
                df_pheno = pd.read_csv(uploaded_file_pheno)
            else:
                df_pheno = pd.read_excel(uploaded_file_pheno)

            df_pheno.columns = df_pheno.columns.str.strip()

            df_pheno["week"] = pd.to_datetime(df_pheno["week"], errors="coerce")
            df_pheno = df_pheno.dropna(subset=["week"])
            df_pheno["Week"] = df_pheno["week"].dt.date

            phenos = ["MRSA", "Other", "VRSA", "Wild"]
            df_pheno["Total"] = df_pheno[phenos].sum(axis=1)
            for pheno in phenos:
                df_pheno[f"% {pheno}"] = (df_pheno[pheno] / df_pheno["Total"]) * 100

            selected_pheno = st.selectbox("Sélectionner un phénotype", phenos)
            min_date, max_date = df_pheno["Week"].min(), df_pheno["Week"].max()
            date_range = st.slider("Plage de semaines", min_date, max_date, (min_date, max_date))

            filtered_pheno = df_pheno[(df_pheno["Week"] >= date_range[0]) & (df_pheno["Week"] <= date_range[1])]
            pct_col = f"% {selected_pheno}"
            values = filtered_pheno[pct_col].dropna()
            q1, q3 = np.percentile(values, [25, 75])
            iqr = q3 - q1
            lower, upper = max(q1 - 1.5 * iqr, 0), q3 + 1.5 * iqr

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=filtered_pheno[pct_col],
                                     mode='lines+markers', name=pct_col))
            fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=[upper]*len(filtered_pheno),
                                     mode='lines', name="Seuil haut", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=filtered_pheno["Week"], y=[lower]*len(filtered_pheno),
                                     mode='lines', name="Seuil bas", line=dict(dash='dot')))
            fig.update_layout(yaxis=dict(range=[0, 100]), xaxis_title="Semaine", yaxis_title="Résistance (%)")
            st.plotly_chart(fig, use_container_width=True)

            nb_tests = filtered_pheno[pct_col].count()
            moyenne = filtered_pheno[pct_col].mean()
            semaine_pic = filtered_pheno.loc[filtered_pheno[pct_col].idxmax(), "Week"]

            st.markdown("### 🧾 Résumé")
            st.write(f"🔢 **Nombre de semaines analysées** : {nb_tests}")
            st.write(f"📊 **Moyenne de {selected_pheno}** : {moyenne:.2f} %")
            st.write(f"💥 **Semaine avec le pic de {selected_pheno}** : {semaine_pic}")

            last_val = filtered_pheno[pct_col].dropna().iloc[-1]
            if last_val > upper:
                st.error(f"🚨 Alerte : taux élevé de {selected_pheno} cette semaine ({last_val:.2f} %)")
            elif last_val < lower:
                st.warning(f"⚠️ Taux anormalement bas de {selected_pheno} cette semaine ({last_val:.2f} %)")
            else:
                st.success(f"✅ Taux de {selected_pheno} dans la norme cette semaine ({last_val:.2f} %)")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les données.")


# === Onglet 4 : Fiches Bactéries ===
with tab4:
    st.header("🧫 Détail des bactéries à étudier")
    uploaded_file_bact = st.file_uploader("📂 Charger un fichier de bactéries à étudier", type=["xlsx"], key="upload_bact")

    if uploaded_file_bact is not None:
        try:
            df_bact = pd.read_excel(uploaded_file_bact)
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

                st.write("**🧬 Phénotype**")
                st.write(details["Phenotype"])
            else:
                st.info("Aucune bactérie ne correspond à votre recherche.")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les données.")
st.set_page_config(page_title="Tableau de bord unifié", layout="wide")

# Déclaration des onglets
import streamlit as st
import pandas as pd

# Onglets de navigation


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Antibiotiques 2024",
    "Autres Antibiotiques",
    "Phénotypes Staph aureus",
    "Fiches Bactéries",
    "Alertes par service"
])

# === Onglet 5 : Alertes par service ===
with tab5:
    st.header("⚠️ Alertes par service")
    uploaded_file_service = st.file_uploader("📂 Charger un fichier des services (Excel)", type=["xlsx"], key="upload_service")

    if uploaded_file_service is not None:
        try:
            df_service = pd.read_excel(uploaded_file_service)
            df_service.columns = df_service.columns.str.strip()

            if "DATE_ENTREE" not in df_service.columns:
                st.error("❌ Colonne 'DATE_ENTREE' absente du fichier.")
                st.write("Colonnes disponibles :", list(df_service.columns))
                st.stop()

            df_service['DATE_ENTREE'] = pd.to_datetime(df_service['DATE_ENTREE'], errors='coerce')
            df_service['Week'] = df_service['DATE_ENTREE'].dt.isocalendar().week

            unique_weeks = sorted(df_service['Week'].dropna().unique().astype(int))
            selected_week = st.selectbox("📆 Choisir une semaine :", unique_weeks)

            services_week = df_service[df_service['Week'] == selected_week]['LIBELLE_DEMANDEUR'].dropna().unique()
            st.markdown(f"### 🏥 Services ayant généré des analyses en semaine {selected_week}")

            if len(services_week) > 0:
                for s in services_week:
                    st.write(f"🔹 {s}")
            else:
                st.info("Aucun service n’a été enregistré cette semaine.")

        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("📥 Veuillez charger un fichier pour afficher les services par semaine.")
