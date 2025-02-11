from LakehouseConnection import LakehouseConnection
from clientes import transform_clients
from produtos import transform_produtos
from pedidos import transform_pedidos
import pandas as pd

def remover_duplicates(df_silver, data_parquet_bronze, bronze_columns_id):
    temp = "./temp"
    path_temp = f"{temp}/{data_parquet_bronze}.parquet"
    
    df_bronze = pd.read_parquet(path_temp)

    if bronze_columns_id not in df_bronze.columns:
        raise KeyError(f"A coluna '{bronze_columns_id}' não existe no DataFrame Bronze ({data_parquet_bronze})")

    df_bronze = df_bronze.drop_duplicates(subset=[bronze_columns_id])

    if df_silver.empty:
        print(f"A camada Silver está vazia. Inserindo todos os {len(df_bronze)} registros.")
        return df_bronze

    df_bronze[bronze_columns_id] = df_bronze[bronze_columns_id].astype(str)
    df_silver["id"] = df_silver["id"].astype(str)

    df_final = df_bronze[~df_bronze[bronze_columns_id].isin(df_silver["id"])]

    print(f"Registros novos para inserir na Silver ({data_parquet_bronze}): {len(df_final)}")
    return df_final

def transform_data():
    lakehouse = LakehouseConnection()
    
    path_data_clientes = lakehouse.get_data_from_bucket("clientes") 
    path_data_produtos = lakehouse.get_data_from_bucket("produtos")
    path_data_pedidos = lakehouse.get_data_from_bucket("pedidos")
        
    silver_data_cliente = lakehouse.get_data_from_lakehouse("clientes", "silver")
    silver_data_produtos = lakehouse.get_data_from_lakehouse("produtos", "silver")
    silver_data_pedidos = lakehouse.get_data_from_lakehouse("pedidos", "silver")
    

    data_clientes = remover_duplicates(silver_data_cliente, "clientes", "id_cliente")
    data_produtos = remover_duplicates(silver_data_produtos, "produtos", "id_produto")
    data_pedidos = remover_duplicates(silver_data_pedidos, "pedidos", "id_pedido")

    size_data_clientes = data_clientes.shape[0]
    size_data_produtos = data_produtos.shape[0]
    size_data_pedidos = data_pedidos.shape[0]
    
    if size_data_clientes == 0 and size_data_produtos == 0 and size_data_pedidos == 0:
        print("Não há novos dados para inserir na camada Silver.")
        lakehouse.clear_temp(path_data_clientes, path_data_produtos, path_data_pedidos)
        lakehouse.close_connection()
        return
    
    if size_data_clientes > 0:
        data_clientes = transform_clients(data_clientes)
        lakehouse.insert_data_to_lakehouse(data_clientes, "clientes", "silver")
    
    if size_data_produtos > 0:
        data_produtos = transform_produtos(data_produtos)
        lakehouse.insert_data_to_lakehouse(data_produtos, "produtos", "silver")
    
    if size_data_pedidos > 0:
        data_pedidos = transform_pedidos(data_pedidos) 
        lakehouse.insert_data_to_lakehouse(data_pedidos, "pedidos", "silver")
        
    lakehouse.clear_temp(path_data_clientes, path_data_produtos, path_data_pedidos)
    lakehouse.close_connection()
    
    print("✅ Transformação concluída com sucesso!")

if __name__ == "__main__":
    transform_data()
