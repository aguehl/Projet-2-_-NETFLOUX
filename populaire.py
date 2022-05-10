import streamlit as st
import pandas as pd


def app():    

    st.header('Les films les plus populaires')

    #dfmelt_rating = pd.read_csv(r'C:\Users\yyoun\Projet2\dfmelt_rating.csv')
    dfmelt_ratingFR = pd.read_csv(r'C:\Users\yyoun\Projet2\df_Final.csv')
    
    col1, col2, col3, col4 = st.columns(4)

    with col1 : 
        for i in range(0,3) : 
            st.subheader(dfmelt_ratingFR['Films'][i])
            st.image(dfmelt_ratingFR['Img'][i], width=250) 
            st.caption(f"https://www.imdb.com/title/{dfmelt_ratingFR['tconst'][i]}/")

    with col2 : 
        for i in range(3,6) : 
            st.subheader(dfmelt_ratingFR['Films'][i])
            st.image(dfmelt_ratingFR['Img'][i], width=250) 
            st.caption(f"https://www.imdb.com/title/{dfmelt_ratingFR['tconst'][i]}/")

    with col3 : 
        for i in range(6,9) : 
            st.subheader(dfmelt_ratingFR['Films'][i])
            st.image(dfmelt_ratingFR['Img'][i], width=250) 
            st.caption(f"https://www.imdb.com/title/{dfmelt_ratingFR['tconst'][i]}/")

    with col4 : 
        for i in range(9,12) : 
            st.subheader(dfmelt_ratingFR['Films'][i])
            st.image(dfmelt_ratingFR['Img'][i], width=250) 
            st.caption(f"https://www.imdb.com/title/{dfmelt_ratingFR['tconst'][i]}/")
          

    #col1, col2 = st.columns([2, 5])
    #with col1 : 
    #    #st.write(dfmelt_rating['primaryTitle'][0]) 
    #    for i in range(15) :
    #        st.write(dfmelt_ratingFR['title'][i])

    #with col2 : 
    #    #st.write(dfmelt_rating['startYear'][0])
    #    for i in range(15) :
    #        st.write(dfmelt_ratingFR['startYear'][i])
    #st.write(dfmelt_rating[['primaryTitle', 'startYear']])
    














    #st.title('Home')

    #st.write('This is the `home page` of this multi-page app.')

    #st.write('In this app, we will be building a simple classification model using the Iris dataset.')
