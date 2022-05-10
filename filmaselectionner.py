from ast import With
from cProfile import label
from email.policy import default
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from PIL import Image 


def app() : 

    df_title=pd.read_csv(r'C:\Users\yyoun\Projet2\dfF.csv', sep=',',usecols=['tconst','Films','Année','Img','averageRating'])
    occurrence_matrix = pd.read_csv(r'C:\Users\yyoun\Projet2\occurrence_matrix3.csv', sep = ",",usecols=['tconst',"startYear","en","fr","de","es","ko","ja","it",
                                "Action","Adventure","Animation", "Biography","Comedy","Crime","Drama","Family",
                                "Fantasy","Film-Noir","History","Horror","Music","Musical","Mystery","Romance","Sci-Fi",
                                "Sport","Thriller","War","Western", 
                                "0_x","1_x","2_x","3_x","4","5","6","7","8","9","10","11","12","13",
                                "0_y","1_y","2_y","3_y"]) # table avec films en lignes et variables en colonnes


    def Get_Matrix_Reco(tconst):
        distance_matrix = pairwise_distances(occurrence_matrix.iloc[:,1:49], occurrence_matrix[["startYear","en","fr",
                                                                                                "de","es","ko","ja",
                                                                                                "it","Action",
                                                                                                "Adventure","Animation",
                                                                                                "Biography","Comedy",
                                                                                                "Crime","Drama","Family",
                                                                                                "Fantasy","Film-Noir",
                                                                                                "History","Horror",
                                                                                                "Music","Musical","Mystery",
                                                                                                "Romance","Sci-Fi",
                                                                                                "Sport","Thriller",
                                                                                                "War","Western",
                                                                                                "0_x","1_x","2_x","3_x","4","5",
                                                                                                "6","7","8","9","10","11",
                                                                                                "12","13",
                                                                                                "0_y","1_y","2_y","3_y"]][occurrence_matrix["tconst"] == tconst],metric = "canberra") # metrique de distance au choix; canberra 
        distance_matrix = pd.DataFrame(distance_matrix)
        distance_matrix["tconst"] = occurrence_matrix["tconst"] # rejoute les tconst des films
        distance_matrix = pd.merge(distance_matrix, df_title[["Films", "averageRating"]], how = "inner", 
                                left_on = distance_matrix.tconst, right_on = df_title.tconst) # rajoute les titres et les ratings
        distance_matrix["distance"] = distance_matrix.iloc[:,1]
        distance_matrix=distance_matrix[distance_matrix.tconst!=tconst]
        distance_matrix = distance_matrix.iloc[:,:].sort_values(by = "distance")
        distance_matrix = distance_matrix.iloc[0:11,:] # retourne les n films les plus proches; n = 10
        return(distance_matrix[["tconst"]])

    df_title['year']=df_title['Année'].apply(lambda x: str(x))

    ### Variables
    df_choice=pd.DataFrame()
    Titre=''

    #st. set_page_config(layout="wide")

    # Case de saisie du titre
    st.header('Saisissez un titre de film')
    Titre=st.text_input(label='', value='')

    if Titre !='':
            
        df_choice=df_title[df_title.Films.str.contains(f'(?i){Titre}')]
        
        if len(df_choice)==0:
            st.subheader("Merci de vérifier l'orthographe du titre")
        else:
            df_choice.sort_values(['Films', 'Année'], inplace=True)

            df_choice['Affiche']=df_choice['Films']+ ' ___ ' + df_choice['year']+ ' ___ '


            Titre_Choice=''
            Titre_Choice = st.selectbox(
                'Quel films exactement?',
                (df_choice.Affiche))

            if Titre_Choice!='':

                titre=Titre_Choice.split(' ___ ')
                #st.write(titre)

                tconst=df_choice.tconst[(df_choice.Films==titre[0])&(df_choice.year==titre[-2])].values[0]
                Image=df_choice.Img[(df_choice.Films==titre[0])&(df_choice.year==titre[-2])].values[0]

                df_Reco= Get_Matrix_Reco(tconst)

                dfaff=df_Reco.merge( df_title[['tconst','Films','averageRating','Img']], on='tconst', how='left')
                dfaff.drop_duplicates(inplace=True)
        
                Col8, Col9, Col10=st.columns([5,5,5])
                with Col9:
                    st.title(titre[0])
                    st.image(Image, width=300 )
                    st.subheader(f'https://www.imdb.com/title/{tconst}/')

                st.title('')
                st.title('Voici des films similaires:')



                Col1, Col2, Col3, Col4=st.columns([2,2,2,2])

                for i in range (0,len(dfaff.tconst),4):
                    with Col1:
                        st.subheader(dfaff.Films.iloc[i])
                        st.image(dfaff.Img.iloc[i], width=250 )
                        st.caption(f'https://www.imdb.com/title/{dfaff.tconst.iloc[i]}/')

                    if i+1<len(dfaff.tconst):

                        with Col2:
                            st.subheader(dfaff.Films.iloc[i+1])
                            st.image(dfaff.Img.iloc[i+1], width=250 )
                            st.caption(f'https://www.imdb.com/title/{dfaff.tconst.iloc[i+1]}/')
                    if i+2<len(dfaff.tconst):
                        with Col3:
                            st.subheader(dfaff.Films.iloc[i+2])
                            st.image(dfaff.Img.iloc[i+2], width=250 )
                            st.caption(f'https://www.imdb.com/title/{dfaff.tconst.iloc[i+2]}/')
                    if i+3<len(dfaff.tconst):
                        with Col4:
                            st.subheader(dfaff.Films.iloc[i+3])
                            st.image(dfaff.Img.iloc[i+3], width=250 )
                            st.caption(f'https://www.imdb.com/title/{dfaff.tconst.iloc[i+3]}/')            



                st.balloons()