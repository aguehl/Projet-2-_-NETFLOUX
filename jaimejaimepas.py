import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from PIL import Image
import random 



def app():

    dico={}
    valide = False
    reco = False

    if st.session_state.flag == False :
        st.session_state.Films = pd.read_csv(r'C:\Users\yyoun\Projet2\Films.csv')
        st.session_state.Films = st.session_state.Films.sample(frac=1).reset_index(drop=True)
        
        st.session_state.flag = True

    if valide == False : 

        st.header('Vos recommandations personnelles')
        st.subheader('')
        col21, col22, col23, col24 = st.columns([2, 3, 2, 3])

        with col21 : 
            for i in range(23) :
                st.image(st.session_state.Films['Img'][i], width=95)

        with col22 : 

            for i in range(23) :
                film1= st.radio(
                st.session_state.Films['Films'][i],
                ('Like', 'Dislike', 'Unknown'), index=2)
                st.caption("")
                st.write("")

                if film1 == 'Like':
                    dico[st.session_state.Films['tconst'][i]] = "Like"

                elif film1 == 'Dislike':
                    dico[st.session_state.Films['tconst'][i]] = "DisLike"   
        with col23 :
            for i in range(23, len(st.session_state.Films)) :
                st.image(st.session_state.Films['Img'][i], width=95)

        with col24 :
            for i in range(23, len(st.session_state.Films)) :
                film2= st.radio(
                st.session_state.Films['Films'][i],
                ('Like', 'Dislike', 'Unknown'), index=2)
                st.caption("")
                st.write("")

                if film2 == 'Like':
                    dico[st.session_state.Films['tconst'][i]] = "Like"

                elif film2 == 'Dislike':
                    dico[st.session_state.Films['tconst'][i]] = "DisLike"               

                

        val = st.button('Validez votre sélection')
        if val :
            reco=True 
            valide = True
            st.session_state.dicofinal=dico
                   

    if reco == True : 

        df_title=pd.read_csv(r'C:\Users\yyoun\Projet2\Titre_FR.csv', sep=',',usecols=['tconst','title','averageRating','Img'])

        #df_vote=pd.read_csv(r'C:\Temp\Projet_2\CSV\Vote_imdb.csv', sep=',')
        #df_like=df_vote[(df_vote.rating>=4)&(df_vote.imdb_rating>=7)]         # Rating>=4 & imdbrating>7 : ils ont aimé et le film est bon sur ImdB
        #df_dislike=df_vote[(df_vote.rating<=2)&(df_vote.imdb_rating<=3)]        # Rating<2& imdbrating<3 : ils n'ont pas aimé le film et le film est bon  pas sur ImdB

        df_like=pd.read_csv(r'C:\Users\yyoun\Projet2\Vote_Like_7.csv', sep=',',usecols=['tconst','userId'])
        df_dislike=pd.read_csv(r'C:\Users\yyoun\Projet2\Vote_Dislike_3.csv', sep=',',usecols=['tconst','userId'])

        occurrence_matrix = pd.read_csv(r'C:\Users\yyoun\Projet2\occurrence_matrix3.csv', sep = ",",usecols=['tconst',"startYear","en","fr","de","es","ko","ja","it",
                                    "Action","Adventure","Animation", "Biography","Comedy","Crime","Drama","Family",
                                    "Fantasy","Film-Noir","History","Horror","Music","Musical","Mystery","Romance","Sci-Fi",
                                    "Sport","Thriller","War","Western", 
                                    "0_x","1_x","2_x","3_x","4","5","6","7","8","9","10","11","12","13",
                                    "0_y","1_y","2_y","3_y"]) # table avec st.session_state.Films en lignes et variables en colonnes
        #tconst_short = pd.read_csv("Titre_FR.csv", sep = ",", usecols=['tconst']) # table totale des st.session_state.Films 

        #Init des variables et dataframe
        nbUser = 100                #Nb d'User utilisés pour proposer des st.session_state.Films
        nbProp = 10                 #Nb de film à proposer en retour

        #note=[5.,4.5,4.,3.5]     # selectrion des bonnes notes >3

        Profil_user_factis={'tt0126004': 'Dislike', 'tt0047947': None, 'tt0167261': 'Dislike', 'tt0399201': None, 'tt0310741': 'Dislike', 'tt0465436': None, 'tt0819755': 'Dislike', 'tt1727252': 'Dislike', 'tt0218616': None, 'tt0454931': 'Like', 'tt0101449': None, 'tt0042779': 'Like', 'tt0075683': None, 'tt0371775': 'Dislike', 'tt0065462': 'Like', 'tt0052618': None, 'tt1038919': None, 'tt1701215': None, 'tt0053946': 'Like', 'tt0068646': None, 'tt0326036': None, 'tt0415965': 'Like', 'tt0081662': None, 'tt0103791': 'Dislike', 'tt0062512': None, 'tt0052354': None, 'tt0841925': None, 'tt2086799': 'Like', 'tt0075774': 'Like', 'tt0096953': 'Like'}
        #liste Tconst Antoine:
        Tconst_Ant={'tt0110413':'Like','tt0119116':'Like', 'tt0357111':'Like', 'tt0105793':'Like', 'tt0078788': 'Like', 'tt0250223': 'Like', 'tt3759416':'Like','tt0109440':'Like','tt2239822':'Like', 'tt2872732':'Like', 'tt0152930':'Like','tt0182357':'Like', 'tt0092099':'Like', 'tt0371746':'Like', 'tt0848228':'Like', 'tt0082971':'Like'}
        #'tt0119972':'Like', , 'tt2250912':'Like' ne passent pas dans la matrice


        def Get_User_Reco(User_prof):

            df_Userlike=pd.DataFrame(columns=['userId','tconst'])
            Prop_Tconst=[]

            for tconst, love in User_prof.items():
                if love=='Like':
                    #print('love',tconst)
                    df=df_like[df_like.tconst==tconst]
                    #print(df)
                    df_Userlike=pd.concat([df_Userlike,df]).reset_index(drop=True)
                elif love=='Dislike':
                    #print('love not', tconst)
                    df=df_dislike[df_dislike.tconst==tconst]
                    #print(df)
                    df_Userlike=pd.concat([df_Userlike,df]).reset_index(drop=True)
                

            #print('st.session_state.Films recommandés :')
            df=pd.DataFrame(df_Userlike.userId.value_counts())      #classement des utilisateurs en fonction du nombre de fois où ils sont en accord avec notre USER
            #print(df, (len(df.userId)))
            if len(df.userId)>0:
                if nbUser > len(df.userId):
                    bestUser=list(df.index[:nbUser])                              # On prend les nb meilleurs bestUser
                else:
                    bestUser=list(df.index[:len(df.userId)])

                df_prop= df_like[(df_like.userId.isin(bestUser))]                  #récup de la liste des st.session_state.Films du bestUser

                df_prop=df_prop[~df_prop.tconst.isin(User_prof.keys())]          # on retire les st.session_state.Films q'uon a déja vu
                dftemp2=pd.DataFrame(df_prop.tconst.value_counts())


                i=0
                while len(Prop_Tconst)<(len(User_prof)*10):
                    Prop_Tconst.append(dftemp2.index[i])
                    i+=1
                #for i in range(len(Prop_Tconst)):
                    #print( Prop_Tconst[i],' : ',df_title.title[df_title.tconst ==Prop_Tconst[i]] )
                return(pd.DataFrame(Prop_Tconst, columns=['tconst']))
            else:
                #print('Profil vide')
                return(None    )
            

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
            distance_matrix["tconst"] = occurrence_matrix["tconst"] # rejoute les tconst des st.session_state.Films
            distance_matrix = pd.merge(distance_matrix, df_title[["title", "averageRating"]], how = "inner", 
                                    left_on = distance_matrix.tconst, right_on = df_title.tconst) # rajoute les titres et les ratings
            distance_matrix["distance"] = distance_matrix.iloc[:,1]
            distance_matrix=distance_matrix[distance_matrix.tconst!=tconst]
            distance_matrix = distance_matrix.iloc[:,:].sort_values(by = "distance")
            distance_matrix = distance_matrix.iloc[0:11,:] # retourne les n st.session_state.Films les plus proches; n = 10
            return(distance_matrix[["tconst"]])


        def Get_Reco(Tconst_Dict):          # en entrée on reçoit un dictionnaire avec (tconst : 'Like') les coix  ['Like',None, 'Dislike']
            Reco=pd.DataFrame()
            
            for tconst, love in Tconst_Dict.items():
                if love=='Like':
                    #print('--- Matrix input',tconst)
                    Matrix_Reco=Get_Matrix_Reco(tconst)
                    #print('=== Reco Matrix', Matrix_Reco)
                    Reco=pd.concat([Reco, Matrix_Reco ])
            #print('=== Reco Matrix TOTAL',Reco)
            
            User_reco=Get_User_Reco(Tconst_Dict)

            
            #print('=== Reco Users', User_reco)
            Reco=pd.concat([Reco, User_reco])
            Reco.rename(columns={0:'tconst'}, inplace=True)
            Reco=Reco[~Reco.tconst.isin(Tconst_Dict.keys())]
            #print(Reco)
            df= Reco.value_counts().reset_index()
            df.rename(columns={0:'nb occurence'}, inplace=True)
            dfaff=df.merge( df_title[['tconst','title','averageRating','Img']], on='tconst', how='left')
            dfaff.sort_values(['nb occurence','averageRating'], ascending=False)
            dfaff.drop_duplicates(inplace=True)
                
            return(dfaff)

        #simulation de profil Uset
        if st.session_state.dicofinal!={}:

            df_aff=Get_Reco(st.session_state.dicofinal)
            #st. set_page_config(layout="wide")

            st.title('Vos Films sont là!')

            Col1, Col2, Col3, Col4=st.columns([2,2,2,2])

            for i in range (0,len(df_aff.tconst),4):
                with Col1:
                    st.subheader(df_aff.title[i])
                    st.image(df_aff.Img.iloc[i], width=250 )
                    st.caption(f'https://www.imdb.com/title/{df_aff.tconst.iloc[i]}/')

                if i+1<len(df_aff.tconst):

                    with Col2:
                        st.subheader(df_aff.title[i+1])
                        st.image(df_aff.Img.iloc[i+1], width=250 )
                        st.caption(f'https://www.imdb.com/title/{df_aff.tconst.iloc[i+1]}/')
                if i+2<len(df_aff.tconst):
                    with Col3:
                        st.subheader(df_aff.title[i+2])
                        st.image(df_aff.Img.iloc[i+2], width=250 )
                        st.caption(f'https://www.imdb.com/title/{df_aff.tconst.iloc[i+2]}/')
                if i+3<len(df_aff.tconst):
                    with Col4:
                        st.subheader(df_aff.title[i+3])
                        st.image(df_aff.Img.iloc[i+3], width=250 )
                        st.caption(f'https://www.imdb.com/title/{df_aff.tconst.iloc[i+3]}/')   



                st.balloons()
                

