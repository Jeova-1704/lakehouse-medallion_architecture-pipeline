from dotenv import load_dotenv
from os import getenv
from supabase import create_client
import math

class Extract:
    def __init__(self):
        load_dotenv()
        self.url = getenv("SUPABASE_URL")
        self.key = getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key)
        self.batch_size = 10_000
        
    def get_data(self, table_name):
        all_data = []
        offset = 0
        
        while True:
            try:
                response = self.client.schema("public").table(table_name).select("*").range(offset, offset + self.batch_size - 1).execute()
                batch_data = response.data

                if not batch_data:
                    break
                    
                all_data.extend(batch_data)
                offset += self.batch_size

                print(f"Extraindo dados da tabela {table_name} - {offset} registros extraídos.")
                
            except Exception as e:
                print(f"Erro ao extrair dados da tabela {table_name}")
                print(e)
                break
            
        print(f"Extração de dados da tabela {table_name} finalizada.")
        return all_data
    
    def close_connection(self):
        self.client = None
        
        
class LoadToLakehouse():
    def __init__(self):
        load_dotenv()
        self.url = getenv("LAKEHOUSE_URL")
        self.key = getenv("LAKEHOUSE_KEY")
        self.client = create_client(self.url, self.key)
        self.batch_size = 10_000

    def close_connection(self):
        self.client = None

    def insert_to_lakehouse(self, data, table_name):
        total_rows = len(data)
        
        if total_rows == 0:
            print(f"Não há dados para inserir na tabela {table_name}")
            return
        
        total_batches = math.ceil(total_rows / self.batch_size)
        
        print(f"Inserindo dados na tabela {table_name}, um total de {total_rows} registros serão inseridos em {total_batches} lotes.")
        
        for i in range(0, total_rows, self.batch_size):
            batch_data = data[i:i + self.batch_size]
            
            try:
                self.client.schema("bronze").table(table_name).insert(batch_data).execute()
                print(f"Inserindo dados na tabela {table_name} - {i + len(batch_data)} registros inseridos.")
            except Exception as e:
                print(f"Erro ao inserir dados na tabela {table_name}")
                print(e)
                break
            
        print(f"Sucesso ao inserir os dados na tabela: {table_name}")
     

def main():
    extract = Extract()
    load = LoadToLakehouse()
    
    data_cliente = extract.get_data("clientes")
    print("Dados do cliente extraídos com sucesso")
    print(f"Quantidade de registros: {len(data_cliente)}")
    data_produto = extract.get_data("produtos") 
    print("Dados do produto extraídos com sucesso")
    print(f"Quantidade de registros: {len(data_produto)}")
    data_pedido = extract.get_data("pedidos")
    print("Dados do pedido extraídos com sucesso")
    print(f"Quantidade de registros: {len(data_pedido)}")
    
    load.insert_to_lakehouse(data_cliente, "clientes")
    load.insert_to_lakehouse(data_produto, "produtos")
    load.insert_to_lakehouse(data_pedido, "pedidos")
    
    print(len(data_cliente))
    
    print("Data inserted successfully")
    
    extract.close_connection()
    load.close_connection()


if __name__ == "__main__":
    main()