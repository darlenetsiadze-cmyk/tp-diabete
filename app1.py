import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Dia-Collect 232 - Darlene", page_icon="🩺", layout="wide")

def charger_donnees():
    if os.path.isfile('donnees_diabete.csv'):
        # On lit le fichier sans index pour éviter les colonnes inutiles
        return pd.read_csv('donnees_diabete.csv')
    return None

# --- 2. STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
    }
    [data-testid="stForm"] {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRE LATÉRALE (IDENTIFICATION) ---
st.sidebar.title("🩺 INF 232 EC2")
st.sidebar.subheader("Identification")
st.sidebar.info(f"""
**Nom :** TSIADZE DONFACK DARLENE  
**Matricule :** 24G2361  
**Filière :** Informatique L2  
**Université de Yaoundé I**
""")

# --- 4. ENTÊTE PRINCIPALE ---
st.title("🩺 Dia-Collect 232 : Système d'Analyse Descriptive")
st.markdown("---")

# --- 5. NAVIGATION PAR ONGLETS ---
tab1, tab2, tab3 = st.tabs(["📝 Collecte", "📊 Analyse Descriptive", "💡 Note Conceptuelle"])

# --- ONGLET 1 : COLLECTE DES DONNÉES ---
with tab1:
    st.subheader("📝 Enregistrement des données cliniques")
    
    with st.form("form_patient", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Identifiant Patient (Anonymisé)", placeholder="Ex: P-2026-001")
            age = st.number_input("Âge du patient", 0, 120, 25)
            genre = st.selectbox("Genre", ["Masculin", "Féminin", "Autre"])
            
        with col2:
            poids = st.number_input("Poids (kg)", 1.0, 250.0, 70.0)
            taille = st.number_input("Taille (m)", 0.5, 2.5, 1.70)
            glycemie = st.number_input("Glycémie (g/L)", 0.1, 6.0, 1.0, step=0.1)
            
        # Calcul automatique de l'IMC
        imc = round(poids / (taille ** 2), 2)
        tension = st.slider("Pression Artérielle (mmHg)", 40, 250, 120)
        
        submitted = st.form_submit_button("🚀 Valider et Enregistrer")
        
        if submitted:
            if nom == "":
                st.error("L'identifiant est obligatoire.")
            else:
                nouvelle_ligne = {
                    "Nom": nom, "Age": age, "Genre": genre, 
                    "IMC": imc, "Glycemie": glycemie, "Tension": tension
                }
                df_nouveau = pd.DataFrame([nouvelle_ligne])
                
                # Sauvegarde dans le fichier CSV
                if not os.path.isfile('donnees_diabete.csv'):
                    df_nouveau.to_csv('donnees_diabete.csv', index=False)
                else:
                    df_nouveau.to_csv('donnees_diabete.csv', mode='a', header=False, index=False)
                
                st.success(f"✅ Patient {nom} enregistré avec succès ! (IMC calculé : {imc})")

# --- ONGLET 2 : ANALYSE DESCRIPTIVE ---
with tab2:
    st.header("📊 Tableau de bord statistique")
    data = charger_donnees()
    
    if data is not None and not data.empty:
        st.subheader("🔍 Analyse par segmentation")
        
        # Filtres interactifs
        genres_filtre = st.multiselect("Filtrer par Genre :", 
                                      options=data['Genre'].unique(), 
                                      default=data['Genre'].unique())
        
        data_filtree = data[data['Genre'].isin(genres_filtre)]
        
        # Indicateurs clés
        c1, c2, c3 = st.columns(3)
        c1.metric("Effectif (N)", len(data_filtree))
        c2.metric("Glycémie Moyenne", f"{data_filtree['Glycemie'].mean():.2f} g/L")
        c3.metric("Âge Moyen", f"{int(data_filtree['Age'].mean())} ans")
        
        st.markdown("---")
        
        # Graphiques
        g1, g2 = st.columns(2)
        
        with g1:
            st.subheader("Structure par Genre (Univariée)")
            fig_pie = px.pie(data_filtree, names='Genre', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.caption("📌 **Explication :** Ce graphique permet de vérifier si l'échantillon collecté est équilibré entre les genres.")
            
        with g2:
            st.subheader("Corrélation IMC vs Glycémie (Bivariée)")
            fig_scatter = px.scatter(data_filtree, x="IMC", y="Glycemie", 
                                     color="Genre", size="Age", hover_name="Nom")
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.caption("📌 **Explication :** Visualisation de l'impact de l'IMC sur le taux de sucre dans le sang.")

        with st.expander("📂 Consulter la base de données complète"):
            st.dataframe(data_filtree, use_container_width=True)
    else:
        st.warning("⚠️ Aucune donnée n'a encore été enregistrée. Utilisez l'onglet Collecte pour commencer.")

# --- ONGLET 3 : NOTE CONCEPTUELLE ---
with tab3:
    st.header("💡 Note Technique & Conceptuelle")
    st.markdown(f"""
    ### 🎯 Objectifs de l'Analyse (UE INF 232)
    * **Collecte Digitale :** Remplacement des formulaires papier par une interface web robuste.
    * **Analyse Univariée :** Étude de la répartition des patients par genre.
    * **Analyse Bivariée :** Recherche de liens statistiques entre l'IMC et la Glycémie.
    
    ---
    **Étudiante :** TSIADZE DONFACK DARLENE  
    **Matricule :** 24G2361  
    **Enseignant :** Pr. Rollin Francis  
    **Institution :** Université de Yaoundé I
    """)
