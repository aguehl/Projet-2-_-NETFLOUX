import streamlit as st
import pandas as pd

def app() : 

    df_Name=pd.read_csv(r'C:\Users\yyoun\Projet2\Name_tconst.csv', sep=',')
    df_Film=pd.read_csv(r'C:\Users\yyoun\Projet2\DfF.csv', sep=',')
    df_Link=pd.read_csv(r'C:\Users\yyoun\Projet2\principalModified_29k.csv', sep=',')

    ### Variables
    df_choice=pd.DataFrame()
    Nom=''
    Name= []
    Cat=[]
    nconst = []
    #st.set_page_config(layout="wide")

    # Case de saisie du Nom
    st.header('Saisissez un nom')
    Nom=st.text_input(label='')

    if Nom != '':
        df_choice=df_Name[df_Name.primaryName.str.contains(f'(?i){Nom}')]
        df_choice.sort_values(['primaryName'], inplace=True)
        if len(df_choice.nconst)==0:
            st.title("Merci de vérifier l'orthographe du Nom")
        
        else:
            Name=st.multiselect('Quel Nom:',df_choice.primaryName.unique())
            if len(Name)>0:
                nconst=list(df_choice.nconst[df_choice.primaryName==Name[0]].unique())
                #st.write(nconst)
                df_choice=df_choice[df_choice.nconst.isin(nconst)]

                # Selection du genre Acteur/Réalisateur
            
                Cat=st.multiselect("",df_choice['Catégorie'].unique())

                if len(Cat)>0:
                        
                    df_choice=df_choice[df_choice['Catégorie'].isin(Cat)]
                    df_tconst=df_Link.tconst[(df_Link.nconst.isin(df_choice.nconst)) & (df_Link['Catégorie'].isin(Cat))]
                    df_Sel=df_Film[df_Film.tconst.isin(df_tconst.unique())]
                    
                    df_Sel.sort_values(['averageRating'],ascending=False ,inplace=True)

                    Col1, Col2, Col3, Col4=st.columns([2,2,2,2])

                    for i in range (0,len(df_Sel.tconst),4):
                        with Col1:
                            st.subheader(df_Sel.Films.iloc[i])
                            st.image(df_Sel.Img.iloc[i], width=250)
                            st.caption(f'https://www.imdb.com/title/{df_Sel.tconst.iloc[i]}/')

                        if i+1<len(df_Sel.tconst):

                            with Col2:
                                st.subheader(df_Sel.Films.iloc[i+1])
                                st.image(df_Sel.Img.iloc[i+1], width=250)
                                st.caption(f'https://www.imdb.com/title/{df_Sel.tconst.iloc[i+1]}/')
                        if i+2<len(df_Sel.tconst):
                            with Col3:
                                st.subheader(df_Sel.Films.iloc[i+2])
                                st.image(df_Sel.Img.iloc[i+2], width=250)
                                st.caption(f'https://www.imdb.com/title/{df_Sel.tconst.iloc[i+2]}/')
                        if i+3<len(df_Sel.tconst):
                            with Col4:
                                st.subheader(df_Sel.Films.iloc[i+3])
                                st.image(df_Sel.Img.iloc[i+3], width=250)
                                st.caption(f'https://www.imdb.com/title/{df_Sel.tconst.iloc[i+3]}/')