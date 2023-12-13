import pandas as pd

def etl_funcao(diretorio_dados):
    df = pd.read_csv(diretorio_dados)
    df1 = df.copy()

    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = df1['Delivery_person_Age'] != None
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    ### Remover espaços vazios strip em toda a tabela
    tipos_de_dados = df.dtypes
    df1 = df1.reset_index(drop=True) # Quando remove-se linhas ele também mata a linha do index.
    for column, tipo in tipos_de_dados.items():
        if tipo == 'object':
            df1[column] = df[column].str.strip()

    ### ============================= 
    ### Remover linhas NaN de várias colunas
    ### =============================
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1.dropna(subset=['Delivery_person_Age'], inplace=True)

    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1.dropna(subset=['multiple_deliveries'], inplace=True)

    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1.dropna(subset=['Road_traffic_density'], inplace=True)

    linhas_selecionadas = df1['City'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1.dropna(subset=['City'], inplace=True)

    linhas_selecionadas = df1['Festival'] != 'NaN'
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1.dropna(subset=['Festival'], inplace=True)



    ### Removendo o texto inteiro da coluna de Time_taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'\(min\)', '', regex=True)

    ### Converter colunas
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1