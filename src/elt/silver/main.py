from LakehouseConnection import LakehouseConnection
from clientes import transform_clients
from produtos import transform_produtos
from pedidos import transform_pedidos

def transform_data():
    lakehouse = LakehouseConnection()
    # data_clientes = lakehouse.get_data_from_lakehouse("clientes", "bronze")
    # data_produtos = lakehouse.get_data_from_lakehouse("produtos", "bronze")
    data_pedidos = lakehouse.get_data_from_lakehouse("pedidos", "bronze")
    
    # data_clientes = transform_clients(data_clientes)
    # data_produtos = transform_produtos(data_produtos)
    data_pedidos = transform_pedidos(data_pedidos)
    
    # lakehouse.insert_data_to_lakehouse(data_clientes, "clientes", "silver")
    # lakehouse.insert_data_to_lakehouse(data_produtos, "produtos", "silver")
    lakehouse.insert_data_to_lakehouse(data_pedidos, "pedidos", "silver")
    print("funcionou")
    
if __name__ == "__main__":
    transform_data()