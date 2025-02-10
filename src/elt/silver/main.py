from LakehouseConnection import LakehouseConnection
from clientes import transform_clients
from produtos import transform_produtos
from pedidos import transform_pedidos

def transform_data():
    lakehouse = LakehouseConnection()
    
    path_data_clientes = lakehouse.get_data_from_bucket("clientes") 
    path_data_produtos = lakehouse.get_data_from_bucket("produtos")
    path_data_pedidos = lakehouse.get_data_from_bucket("pedidos")
        
    data_clientes = transform_clients(path_data_clientes)
    data_produtos = transform_produtos(path_data_produtos)
    data_pedidos = transform_pedidos(path_data_pedidos)
    
    lakehouse.insert_data_to_lakehouse(data_clientes, "clientes", "silver")
    lakehouse.insert_data_to_lakehouse(data_produtos, "produtos", "silver")
    lakehouse.insert_data_to_lakehouse(data_pedidos, "pedidos", "silver")
    
    lakehouse.clear_temp(path_data_clientes, path_data_produtos, path_data_pedidos)
    lakehouse.close_connection()
    print("funcionou")
    
if __name__ == "__main__":
    transform_data()