import pandas as pd


def transform_data_type_clientes(df):
    df["idade"] = df["idade"].astype(int)
    return df


def drop_columns(df):
    df.drop(columns=['load_timestamp', 'process_id', 'row_version'], inplace=True)
    return df
    

def null_check(df): 
    null_values = df.isnull().sum()
    print(null_values)
    return null_values


def transform_clients(data):
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
    df = transform_data_type_clientes(df)

    print("=====================================")
    print("Removendo colunas desnecessárias")
    df = drop_columns(df)

    print("=====================================")
    print("Transformação de clientes concluída!")

    return df
