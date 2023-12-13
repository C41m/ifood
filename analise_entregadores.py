import plotly.express as px
import folium
import pandas as pd
import numpy as np

def idade_func(df1):
    df_aux_max = df1.loc[:, 'Delivery_person_Age'].max()
    df_aux_min = df1.loc[:, 'Delivery_person_Age'].min()
    return df_aux_min, df_aux_max

def condicao_veiculo_func(df1):
    df_aux_cond_vei_max = df1.loc[:, 'Vehicle_condition'].max()
    df_aux_cond_vei_min = df1.loc[:, 'Vehicle_condition'].min()
    return df_aux_cond_vei_min, df_aux_cond_vei_max

def med_ent_func(df1):
    df_aux_med_ent = df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
    return df_aux_med_ent

def med_desv_tra_func(df1):
    df_aux_med_desv_tra = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean', 'std']})

    # Mudar nomes das colunas
    df_aux_med_desv_tra.columns = ['Média', 'Desvio Pad']
    df_aux_med_desv_tra = df_aux_med_desv_tra.reset_index(drop=True)
    return df_aux_med_desv_tra

def med_desv_cli_func(df1):
    df_aux_med_desv_cli = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings': ['mean', 'std']})

    # Mudar nomes das colunas
    df_aux_med_desv_cli.columns = ['Média', 'Desvio Pad']
    df_aux_med_desv_cli = df_aux_med_desv_cli.reset_index(drop=True)
    return df_aux_med_desv_cli

def ent_mais_rap_func(df1):
    df_ent_mais_rap = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['City', 'Time_taken(min)'], ascending=True).reset_index()

    df_aux01 = df_ent_mais_rap.loc[df_ent_mais_rap['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df_ent_mais_rap.loc[df_ent_mais_rap['City'] == 'Urban', :].head(10)
    df_aux03 = df_ent_mais_rap.loc[df_ent_mais_rap['City'] == 'Semi-Urban', :].head(10)

    df_ent_mais_rap = pd.concat( [df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df_ent_mais_rap

def df_ent_mais_len_func(df1):
    df_ent_mais_len = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['City', 'Time_taken(min)'], ascending=False).reset_index()

    df_aux01 = df_ent_mais_len.loc[df_ent_mais_len['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df_ent_mais_len.loc[df_ent_mais_len['City'] == 'Urban', :].head(10)
    df_aux03 = df_ent_mais_len.loc[df_ent_mais_len['City'] == 'Semi-Urban', :].head(10)

    df_ent_mais_len = pd.concat( [df_aux01, df_aux02, df_aux03]).reset_index(drop=True) 
    return df_ent_mais_len