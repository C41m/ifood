from etl import etl_funcao
from analise import  date_filter_func, traffic_options_func
from analise_entregadores import idade_func, condicao_veiculo_func, med_ent_func, med_desv_tra_func, med_desv_cli_func, ent_mais_rap_func, df_ent_mais_len_func
from datetime import datetime
from streamlit_folium import folium_static
import folium
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
diretorio_dados = 'dados/train.csv'
df1 = etl_funcao(diretorio_dados)


st.set_page_config(page_title='Entregadores')

st.title('Marketplace')



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
        st.title('Overall Metrics')

        col1, col2, col3, col4 = st.columns(4, gap='Small')
        idade_min, idade_max = idade_func(df1)
        cond_veic_min, cond_veic_max = condicao_veiculo_func(df1)

        with col1:
            # Maior idade dos entregadores
            st.markdown('#####s Maior Idade')
            st.markdown(f'## {idade_max}')

        with col2:
            # Menor idade dos entregadores
            st.markdown('##### Menor Idade')
            st.markdown(f'## {idade_min}')
      
        with col3:
            # Melhor situação de veículo
            st.markdown('##### Melhor Condição de Veiculos')
            st.markdown(f'## {cond_veic_max}')
        with col4:
            st.markdown('##### Pior Condição de Veiculos')
            st.markdown(f'## {cond_veic_min}')


    with st.container():
        st.markdown('---')
        st.markdown('# Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliações Médias por Entregador')
            df_aux_med_ent = med_ent_func(df1)
            st.dataframe(df_aux_med_ent, use_container_width=True, hide_index=True)
            
        with col2:
            st.markdown('##### Avaliação Média por Trânsito')
            df_aux_med_desv_tra = med_desv_tra_func(df1)
            st.dataframe(df_aux_med_desv_tra, use_container_width=True, hide_index=True)

            st.markdown('##### Avaliação Média por Clima')
            df_aux_med_desv_cli = med_desv_cli_func(df1)
            st.dataframe(df_aux_med_desv_cli, use_container_width=True, hide_index=True)

    with st.container():
        st.markdown('---')
        st.markdown('# Velocidade de Entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### Entregadores Mais Rápidos')
            ent_mais_rap = ent_mais_rap_func(df1)
            st.dataframe(ent_mais_rap, use_container_width=True, hide_index=True)

        with col2:
            st.markdown('### Entregadores Mais Lentos')
            df_ent_mais_len = df_ent_mais_len_func(df1)
            st.dataframe(df_ent_mais_len, use_container_width=True, hide_index=True)
