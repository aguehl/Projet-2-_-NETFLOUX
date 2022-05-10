import streamlit as st
from multiapp import MultiApp
from apps import populaire, selection, jaimejaimepas,  filmaselectionner, acteursreaaselectionner    # import your app modules here
from PIL import Image
import pandas as pd

app = MultiApp()
st. set_page_config(layout="wide")

if 'dicofinal' not in st.session_state : 
        st.session_state.flag = False
        st.session_state.dicofinal = {}
        st.session_state.Films= pd.DataFrame()
        st.session_state.valide = False

Col6, Col7=st.columns([15,2])

with Col7:
    img = Image.open(r"C:\Users\yyoun\Projet2\Images\netfloux_ver_blurr.png") 
    st.image(img, width=150) 

with Col6 : 
    img2 = Image.open(r"C:\Users\yyoun\Projet2\Images\netfloux_header_red_vector.png")
    st.image(img2, width=500)  

#st.markdown("""
# Chez Netfloux
#""")

# Add all your application here
app.add_app("Films les plus populaires", populaire.app)
app.add_app("Votre sélection", selection.app)
app.add_app("Vos recommandations personnelles", jaimejaimepas.app)
app.add_app("Recherche par film", filmaselectionner.app)
app.add_app("Recherche par nom", acteursreaaselectionner.app)

# The main app
app.run()
