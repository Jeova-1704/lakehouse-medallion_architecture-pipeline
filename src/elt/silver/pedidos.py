import pandas as pd

def transform_data_type_pedidos(df):
    df["quantidade"] = df["quantidade"].replace("", pd.NA)
    df["valor_total"] = df["valor_total"].replace("", pd.NA)
    df["data_pedido"] = df["data_pedido"].replace("", pd.NA)
    
    df = df.dropna(subset=["quantidade", "valor_total", "data_pedido"])
    
    df.loc[:, "quantidade"] = df["quantidade"].astype(int)
    df.loc[:, "valor_total"] = df["valor_total"].astype(float)
    
    df.loc[:, "data_pedido"] = pd.to_datetime(df["data_pedido"], errors="coerce").dt.strftime("%Y-%m-%d")
    
    return df


def drop_columns(df):
    df.drop(columns=['load_timestamp', 'process_id', 'row_version'], inplace=True)
    return df
    

def null_check(df): 
    null_values = df.isnull().sum()
    print(null_values)
    return null_values


def transform_pedidos(data):
    df = pd.DataFrame(data)
    
    print("=====================================")
    print("Checando os valores nulos")
    null_check(df)


    print("=====================================")
    print("Checando os valores nulos após a remoção")
    null_check(df)

    print("=====================================")
    print("Verificando a quantidades de valores que ficaram após a remoção dos valores nulos")
    print(df.shape)

    print("=====================================")
    print("Convertendo idade para inteiro")
    df = transform_data_type_pedidos(df)

    print("=====================================")
    print("Removendo colunas desnecessárias")
    df = drop_columns(df)

    print("=====================================")
    print("Transformação de clientes concluída!")

    return df
