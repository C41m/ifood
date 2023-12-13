import plotly.express as px
import folium
import pandas as pd
import numpy as np

def date_filter_func(df1, date_slicer):
    linhas_selecionadas = df1['Order_Date'] < date_slicer
    linhas_selecionadas = df1.loc[linhas_selecionadas, :]
    return linhas_selecionadas

def traffic_options_func(df1, traffic_options):
    linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
    linhas_selecionadas = df1.loc[linhas_selecionadas, :]
    return linhas_selecionadas

def qnt_entregas_fun(df1):
    qte = df1.shape[0]
    return qte

def qnt_pedidos_dia_func(df1):
    cols = ['ID', 'Order_Date']
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
    media = np.mean(df_aux['ID'])

    fig = px.bar(df_aux, x='Order_Date', y='ID')
    fig.add_hline(y=media, line_dash='dot', line_color='white', label=dict(text=f'Média: {media:.2f}', textposition='start', font=dict(size=15)))

    # Personalizar os rótulos dos eixos
    fig.update_layout(
        xaxis_title='Data',
        yaxis_title='Pedidos',
        dragmode=False
    )

    # Personalizar o formato das datas no eixo x
    fig.update_xaxes(
        tickformat='%d/%m/%Y',
        hoverformat='%d/%m/%Y',
        tickangle=90
    )
    # Personalizar a informação exibida ao passar o mouse sobre o gráfico
    fig.update_traces(
        hovertemplate='%{x}<br>Pedidos: %{y}'
    )    
    return fig    

def qnt_pedidos_trafego_func(df1):
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID']/df_aux['ID'].sum()
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density', custom_data=['ID'])
    
    # Personalizar a informação exibida ao passar o mouse sobre o gráfico
    fig.update_traces(
        hovertemplate='Tráfego: %{label}<br>Percentual de Entregas: %{percent}<br>Entregas: %{customdata[0]}'
    )
    return fig

def qnt_pedidos_cidade_trafego_func(df1):
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.bar(df_aux, x='Road_traffic_density', y='ID', color='City')
    
    # Personalizar os rótulos dos eixos
    fig.update_layout(
        xaxis_title='Tráfego',
        yaxis_title='Pedidos',
        dragmode=False
    )
    # Personalizar a informação exibida ao passar o mouse sobre o gráfico
    fig.update_traces(
        hovertemplate='Tráfego: %{x}<br>Pedidos: %{y}<br>Cidade: %{fullData.name}<extra></extra>',
    )
    return fig

# =========================
# tab 2
# =========================

def pedidos_semana_func(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')

    # Remover a seleção no gráfico
    fig.update_layout(
    xaxis_title='Semana do Ano',
    yaxis_title='Pedidos',
    dragmode=False
    )

    # Personalizar a informação exibida ao passar o mouse sobre o gráfico
    fig.update_traces(
        hovertemplate='Semana do Ano: %{x}<br>Pedidos: %{y}<extra></extra>',
    )
    return fig

def pedidos_semana_entregador_func(df1):
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

    df_aux = pd.merge(df_aux01, df_aux02)
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='order_by_delivery')

    # Remover a seleção no gráfico
    fig.update_layout(
    xaxis_title='Semana do Ano',
    yaxis_title='Pedidos por Entregador',
    dragmode=False
    )

    # Personalizar a informação exibida ao passar o mouse sobre o gráfico
    fig.update_traces(
        hovertemplate='Semana do Ano: %{x}<br>Pedidos por Entregador: %{y}<extra></extra>',
    )

    return fig

def map_func(df1):
    df_aux =df1.loc[:,['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
    return map


