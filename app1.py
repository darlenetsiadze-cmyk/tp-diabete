import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Dia-Collect 232 - TSIADZE", page_icon="🩺", layout="wide")

def charger_donnees():
    if os.path.isfile('donnees_diabete.csv'):
        return pd.read_csv('donnees_diabete.csv')
    return None

# --- STYLE CSS ---
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

# --- IDENTIFICATION DANS LA BARRE LATÉRALE (SIDEBAR) ---
st.sidebar.title("🩺 INF 232 EC2")
st.sidebar.subheader("Identification")
st.sidebar.info(f"""
**Nom :** TSIADZE DONFACK DARLENE
**Matricule :** 24G2361 
**Filière :** Informatique L2  
**Université de Yaoundé I**
""")

# --- ENTÊTE ---
st.title("🩺 Dia-Collect 232 : Système d'Analyse Descriptive")
st.markdown("---")

# --- NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📝 Collecte des Données", "📊 Analyse Descriptive", "💡 Note Conceptuelle"])

# --- ONGLET 1 : COLLECTE ---
with tab1:
    st.subheader("📝 Enregistrement des données cliniques")
    with st.form("form_patient", clear_on_submit=True):
        col_id, col_physique, col_bio = st.columns(3)
        with col_id:
            st.markdown("### 🆔 Patient")
            nom = st.text_input("Identifiant (Anonymisé)", placeholder="Ex: P-2026-001")
            age = st.number_input("Âge du patient", 0, 120, 25)
            genre = st.selectbox("Genre", ["Masculin", "Féminin", "Autre"])
        with col_physique:
            st.markdown("### ⚖️ Mesures")
            poids = st.number_input("Poids (kg)", 1.0, 250.0, 70.0)
            taille = st.number_input("Taille (m)", 0.5, 2.5, 1.70)
        with col_bio:
            st.markdown("### 🩸 Santé")
            glycemie = st.number_input("Glycémie (g/L)", 0.1, 6.0, 1.0, step=0.1)
            tension = st.slider("Pression Artérielle (mmHg)", 40, 250, 120)
        st.markdown("---")
        submitted = st.form_submit_button("🚀 VALIDER ET ENREGISTRER")
        if submitted:
            if nom == "":
                st.error("L'identifiant est obligatoire.")
            else:
                imc = round(poids / (taille ** 2), 2)
                nouvelle_ligne = {"Nom": nom, "Age": age, "Genre": genre, "IMC": imc, "Glycemie": glycemie, "Tension": tension}
                df_nouveau = pd.DataFrame([nouvelle_ligne])
                if not os.path.isfile('donnees_diabete.csv'):
                    df_nouveau.to_csv('donnees_diabete.csv', index=False)
                else:
                    df_nouveau.to_csv('donnees_diabete.csv', mode='a', header=False, index=False)
                st.success(f"✅ Patient {nom} enregistré ! (IMC : {imc})")

# --- ONGLET 2 : ANALYSE ---
with tab2:
    st.header("📊 Tableau de bord statistique")
    data = charger_donnees()
    if data is not None:
        st.markdown("#### ⚙️ Paramètres d'affichage")
        col_tri, col_vide = st.columns([1, 2])
        with col_tri:
            tri = st.selectbox("Trier la table par :", ["Nom", "Glycemie", "Age", "IMC"])
        data = data.sort_values(by=tri)
        
        genres_filtre = st.multiselect("Comparer les groupes :", options=data['Genre'].unique(), default=data['Genre'].unique())
        data_filtree = data[data['Genre'].isin(genres_filtre)]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Effectif (N)", len(data_filtree))
        c2.metric("Glycémie Moyenne", f"{data_filtree['Glycemie'].mean():.2f} g/L")
        c3.metric("Âge Moyen", f"{int(data_filtree['Age'].mean())} ans")
        
        st.markdown("---")
        g1, g2 = st.columns(2)
        with g1:
            st.subheader("Structure par Genre (Univariée)")
            st.plotly_chart(px.pie(data_filtree, names='Genre', hole=0.4), use_container_width=True)
            st.caption("📌 **Explication technique :** Ce diagramme permet de vérifier la représentativité de l'échantillon...")
        with g2:
            st.subheader("Corrélation IMC vs Glycémie (Bivariée)")
            st.plotly_chart(px.scatter(data_filtree, x="IMC", y="Glycemie", color="Genre", size="Age"), use_container_width=True)
            st.caption("📌 **Explication technique :** Ce nuage de points analyse si l'IMC influe sur la glycémie...")
        
        with st.expander("📂 Voir la base de données brute"):
            st.dataframe(data_filtree, use_container_width=True)
    else:
        st.warning("⚠️ Aucune donnée disponible.")

# --- ONGLET 3 : NOTE CONCEPTUELLE ---
with tab3:
    st.header("💡 Note Technique & Conceptuelle")
    st.markdown(f"""
    
    ### 🛠️ Choix Techniques (Qualités de l'application) :
    1.  **Créativité :** Intégration d'un calculateur d'IMC automatique et d'une analyse bivariée en temps réel.
    2.  **Robustesse :** Persistance des données via CSV et gestion automatique des tris.
    3.  **Efficacité :** Interface simplifiée permettant une saisie rapide et une visualisation immédiate.
    4.  **Fiabilité :** Algorithmes de calcul basés sur les standards de l'OMS (Organisation Mondiale de la Santé).

    **Secteur d'activité :** Santé Publique - Étude du Diabète.  
    **Étudiante :** TSIADZE DONFACK DARLENE | **Matricule :** [24G2361]  
    **Enseignant :** Pr. Rollin Francis
    
    
    """)
