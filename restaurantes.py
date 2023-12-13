from etl import etl_funcao
from analise import  date_filter_func, traffic_options_func
from analise_restaurantes import qnt_entregadores_func, dist_media_func, desv_pad_fest_func, tempo_med_cidades_func
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
diretorio_dados = 'dados/train.csv'
df1 = etl_funcao(diretorio_dados)


st.set_page_config(page_title='Restaurantes')

st.title('Marketplace - Restaurantes')



# =============================
# Sidebar
# =============================

st.sidebar.title('Caio Fernando Brito Soares')
st.sidebar.title('Entregadores')
st.sidebar.write('---')
st.sidebar.header('Filtros')

date_slicer = st.sidebar.slider(label='Escolha o intervalo das datas',
    min_value=df1['Order_Date'].min().date(),
    max_value=df1['Order_Date'].max().date(),
    format='DD/MM/YYYY', value=df1['Order_Date'].max().date()
    )
date_slicer = datetime.combine(date_slicer, datetime.min.time())

unique_road_density = df1['Road_traffic_density'].unique().tolist()
traffic_options = st.sidebar.multiselect(
    'Condições de trânsito',
    unique_road_density,
    default=unique_road_density, placeholder='Escolha',
)

df1 = traffic_options_func(df1, traffic_options)
df1 = date_filter_func(df1, date_slicer)

st.sidebar.write('---')

# ==============================
# Sidebar Final 
# ==============================



tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.markdown('# Totais')

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            qnt_entregadores = qnt_entregadores_func(df1)
            col1.metric('Qnt Entregadores', qnt_entregadores)

        with col2:
            dist_media = dist_media_func(df1)
            col2.metric('Distância Média', dist_media)

        with col3:
            temp_med_fest = desv_pad_fest_func(df1, 'Tempo Medio', 'Yes')
            col3.metric('Tempo Médio de Entregas durante eventos', temp_med_fest)

        with col4:
            desv_pad_fest = desv_pad_fest_func(df1, 'Desv Padrao', 'Yes')
            col4.metric('Desvio Padrão de Entrega durante eventos', desv_pad_fest)

        with col5:
            temp_med_fest = desv_pad_fest_func(df1, 'Tempo Medio', 'No')
            col3.metric('Tempo Médio de Entregas', temp_med_fest)

        with col6:
            temp_med_fest = desv_pad_fest_func(df1, 'Desv Padrao', 'No')
            col4.metric('Desvio Padrão de Entrega', desv_pad_fest)

        
    with st.container():
        st.markdown('# Tempo Médio de entrega por cidade')
        tempo_med_cidades = tempo_med_cidades_func(df1)
        fig = go.Figure(data=[go.Pie(labels=tempo_med_cidades['City'], values=tempo_med_cidades['distance'], pull=[0, 0.1, 0])])
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('# Distribuição do Tempo')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('OI')

        with col2:
            st.markdown('OI')


    with st.container():
        st.markdown('# Distribuição da Distancia')
