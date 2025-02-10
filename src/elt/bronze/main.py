from dotenv import load_dotenv
from os import getenv, path, remove, makedirs
from supabase import create_client
import math
import pandas as pd 
from datetime import datetime

class Extract:
    def __init__(self):
        load_dotenv()
        self.url = getenv("SUPABASE_URL")
        self.key = getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key)
        self.batch_size = 10_000
        
    def get_data(self, table_name):
        # response = self.client.schema("public").table(table_name).select("*").limit(10).execute()
        # return response.data
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
        self.bucket_name = getenv("BUCKET_NAME")
        self.batch_size = 10_000

    def close_connection(self):
        self.client = None
        
    def insert_to_bucket_storage(self, data, package_name):
        temp = "./temp"
        
        if not path.exists(temp):
            makedirs(temp)
        
        
        if not data:
            print("Não há dados para inserir no bucket.")
            return
        
        df = pd.DataFrame(data)
        
        now = datetime.now()
        ano = now.strftime("%Y")
        mes = now.strftime("%m")
        
        filename = f"{package_name}.parquet"
        bucket_path = f"{ano}/{mes}/{filename}"
        
        temp_file_path = f"{temp}/{filename}"
        
        try:
            df.to_parquet(temp_file_path, index=False)
            
            with open(temp_file_path, "rb") as file:
                response = self.client.storage.from_(self.bucket_name).upload(
                    file=file,
                    path=bucket_path,
                )
            
            print(f"Arquivo {filename} inserido no bucket com sucesso.")
        
        except Exception as e:
            print(f"Erro ao inserir dados no bucket.")
            print(e)
        
        finally:
            if path.exists(temp_file_path):
                remove(temp_file_path)
        
        
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

    load.insert_to_bucket_storage(data_cliente, "clientes")
    load.insert_to_bucket_storage(data_produto, "produtos")
    load.insert_to_bucket_storage(data_pedido, "pedidos")
    
    extract.close_connection()
    load.close_connection()
    
    print("Processo finalizado.")


if __name__ == "__main__":
    main()