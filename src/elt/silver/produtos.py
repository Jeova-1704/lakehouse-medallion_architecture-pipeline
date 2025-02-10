import pandas as pd

def transform_data_type_produtos(df):
    df['preco'] = df['preco'].replace("", pd.NA)
    df = df.dropna(subset=['preco'])
    df['estoque'] = df['estoque'].replace("", pd.NA)
    df = df.dropna(subset=['estoque'])
    df['preco'] = df['preco'].astype(float)
    df['estoque'] = df['estoque'].astype(int)
    return df
    
def null_check(df): 
    null_values = df.isnull().sum()
    print(null_values)
    return null_values

def rename_columns(df):
    df = df.rename(columns={"id_produto": "id"})
    return df

def transform_produtos(df):
    
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
    df = transform_data_type_produtos(df)
    
    print("=====================================")
    print("Renomeando colunas")
    df = rename_columns(df)

    print("=====================================")
    print("Transformação de clientes concluída!")

    return df
