from dotenv import load_dotenv
from os import getenv, path, remove, makedirs
from supabase import create_client
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
                                
            except Exception as e:
                print(f"Erro ao extrair dados da tabela {table_name}")
                print(e)
                break
            
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
        
        path_storage = F"{ano}/{mes}"
        files_storage = self.client.storage.from_(self.bucket_name).list(path_storage)
        
        files_storage = [file["name"] for file in files_storage]

        if filename in files_storage:
            return 135
        
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
        
        return 246
        
        
def main():
    extract = Extract()
    load = LoadToLakehouse()
    
    data_cliente = extract.get_data("clientes")
    
    data_produto = extract.get_data("produtos") 
    
    data_pedido = extract.get_data("pedidos")

    key_permission1: int = load.insert_to_bucket_storage(data_cliente, "clientes")
    key_permission2: int = load.insert_to_bucket_storage(data_produto, "produtos")
    key_permission3: int = load.insert_to_bucket_storage(data_pedido, "pedidos")
    
    extract.close_connection()
    load.close_connection()
    
    if key_permission1 == key_permission2 == key_permission3 == 135:
        print("ERRO AO ARMAZENAR OS DADOS NA CAMADA BRONZE. OS ARQUIVOS JÁ EXISTEM OU FOI EXECUTADO FORA DO PRAZO")
        return 135
    
    print("Sucesso na camada bronze")
    return 246
    


if __name__ == "__main__":
    main()