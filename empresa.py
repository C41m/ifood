from etl import etl_funcao
from analise import qnt_entregas_fun, qnt_pedidos_dia_func, qnt_pedidos_trafego_func, qnt_pedidos_cidade_trafego_func, map_func, date_filter_func, traffic_options_func, pedidos_semana_func, pedidos_semana_entregador_func
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

map = map_func(df1)

st.set_page_config(page_title='Empresa')

st.title('Marketplace')

# with open('styles.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


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

with st.container():
    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Demográfica'])

with tab1:
    with st.container():
        st.markdown('## Total de Entregas')
        qnt_entregas = qnt_entregas_fun(df1)
        st.metric('', qnt_entregas)
        st.markdown('---')

    with st.container():
        st.markdown('## Pedidos por Dia')
        qnt_pedidos_dia = qnt_pedidos_dia_func(df1)
        st.plotly_chart(qnt_pedidos_dia, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
    

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('## Pedidos por tráfego')
            qnt_pedidos_trafego = qnt_pedidos_trafego_func(df1)
            st.plotly_chart(qnt_pedidos_trafego, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown('## Pedidos por tipo de tráfego')
            qnt_pedidos_cidade_trafego = qnt_pedidos_cidade_trafego_func(df1)
            st.plotly_chart(qnt_pedidos_cidade_trafego, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})


with tab2:
    with st.container():
        st.markdown('# Entregas por Semana')
        pedidos_semana = pedidos_semana_func(df1)
        st.plotly_chart(pedidos_semana, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
    
    with st.container():
        st.markdown('# Entregas por Entregador por Semana')
        pedidos_semana_entregador = pedidos_semana_entregador_func(df1)
        st.plotly_chart(pedidos_semana_entregador, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
        
with tab3:
    with st.container():
        st.markdown('# Mapa')
        df_aux =df1.loc[:,['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
        map = folium.Map()

        for index, location_info in df_aux.iterrows():
            folium.Marker( [location_info['Delivery_location_latitude'],
                            location_info['Delivery_location_longitude']],
                            popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
        
        folium_static(map, width=700, height=500)

    
