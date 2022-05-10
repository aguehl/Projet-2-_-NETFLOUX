import streamlit as st
import pandas as pd

def app():


    st.header('Votre sélection')

    df_ex = pd.read_csv(r'C:\Users\yyoun\Projet2\df_exF.csv')
    dfmelt_ratingFR = pd.read_csv(r'C:\Users\yyoun\Projet2\dfF.csv')
    dfmelt_ratingFR.genres = dfmelt_ratingFR.genres.apply(eval)

    options = df_ex['genres'].unique().tolist()
    optionsT = sorted(options)
    select = st.multiselect('Quel genre de film voulez-vous regarder ?', optionsT)
    filtered_df = dfmelt_ratingFR[dfmelt_ratingFR['genres'].apply(lambda gs: any((g in select) for g in gs))]
    #filtered_df = dfmelt_ratingFR[dfmelt_ratingFR['genres'].isin(select)]
    #st.dataframe(filtered_df)

    options2 = df_ex['Decennie'].unique().tolist()
    options2T= sorted(options2)
    select2 = st.multiselect('A quelle période ?', options2T)
    filtered_df2 = filtered_df[filtered_df['Decennie'].isin(select2)]
    #st.dataframe(filtered_df2)

    duremax = st.slider('Quelle sera la durée maximum du film ? (en minutes)', min_value=30 , max_value=300, value=120, step=30)
    st.write("La durée maximal du film sera de ", duremax, "minutes.")
    filtered_df3 = filtered_df2[filtered_df2['runtimeMinutes'] <= duremax]
    if filtered_df3.empty:
        pass
    else:
        st.dataframe(filtered_df3[['Films', 'Année']])










    


