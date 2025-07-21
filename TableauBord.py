import streamlit as st
import sqlite3
import pandas as pd


USERNAME = "admin"
PASSWORD = "1234"

st.title("Connexion...")

username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if username == USERNAME and password == PASSWORD:
    st.success("Connecté avec succès ")

  
    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            date_heure TEXT
        )
    ''')
    conn.commit()

    
    df = pd.read_sql_query("SELECT * FROM detection", conn)

    st.title(" Tableau de bord Surveillance IA2 groupe 1002")

    if df.empty:
        st.info("Aucune détection enregistrée .")
    else:
        noms = ["Tous"] + sorted(df['nom'].unique().tolist())
        selected_nom = st.selectbox("Filtrer par nom", noms)

        if selected_nom != "Tous":
            df = df[df["nom"] == selected_nom]

        st.subheader(" Historique  détections")
        st.dataframe(df)

        
        st.subheader(" Statistiques")
        stats = df['nom'].value_counts().rename_axis('Nom').reset_index(name='Nombre')
        st.bar_chart(stats.set_index('Nom'))

else:
    st.warning("Veuillez entrer des identifiants corrects")
