from dotenv import load_dotenv
<<<<<<< Updated upstream
from os import getenv, path, remove, makedirs
from supabase import create_client
import math
import pandas as pd 
from datetime import datetime
=======
from os import getenv, remove, path
from supabase import create_client
import math
from datetime import datetime
import pandas as pd
import json
import tempfile
>>>>>>> Stashed changes

class Extract:
    def __init__(self):
        load_dotenv()
        self.url = getenv("SUPABASE_URL")
        self.key = getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key)
        self.batch_size = 10_000
        
    def get_data(self, table_name):
<<<<<<< Updated upstream
        # response = self.client.schema("public").table(table_name).select("*").limit(10).execute()
        # return response.data
        all_data = []
        offset = 0
=======
>>>>>>> Stashed changes
        
        response = self.client.schema("public").table(table_name).select("*").limit(10).execute()
        return response.data
        # all_data = []
        # offset = 0
        
        # while True:
        #     try:
        #         response = self.client.schema("public").table(table_name).select("*").range(offset, offset + self.batch_size - 1).execute()
        #         batch_data = response.data

        #         if not batch_data:
        #             break
                    
        #         all_data.extend(batch_data)
        #         offset += self.batch_size

        #         print(f"Extraindo dados da tabela {table_name} - {offset} registros extraídos.")
                
        #     except Exception as e:
        #         print(f"Erro ao extrair dados da tabela {table_name}")
        #         print(e)
        #         break
            
        # print(f"Extração de dados da tabela {table_name} finalizada.")
        # return all_data
    
    def close_connection(self):
        self.client = None
        
        
class LoadToLakehouse():
    def __init__(self):
        load_dotenv()
        self.url = getenv("LAKEHOUSE_URL")
        self.key = getenv("LAKEHOUSE_KEY")
        self.bucket_name = getenv("BUCKET_NAME")
        self.client = create_client(self.url, self.key)
<<<<<<< Updated upstream
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
        timestamp = now.strftime("%Y%m%d_%H%M%S")
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
        
        
=======

    def close_connection(self):
        self.client = None

    def insert_to_bucket_lakehouse(self, data, package_name):
        if len(data) == 0:
            print("Nenhum dado para inserir")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        ano = datetime.now().strftime("%Y")
        mes = datetime.now().strftime("%m")
        
        meta_dados = {
            "package_name": package_name,
            "timestamp": timestamp,
            "quantity": len(data)
        }
        
        json_data = {
            "dados": pd.DataFrame(data).to_dict(orient="records"),
            "meta_dados": meta_dados
        }
        
        filename = f"{package_name}_{file_timestamp}.json"
        bucket_path = f"{ano}/{mes}/{filename}"
        
        temp_dir = tempfile.gettempdir()
        temp_file = path.join(temp_dir, f"{package_name}_{file_timestamp}.json")
        

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
            
        with open(temp_file, "rb") as f:
            self.client.storage.from_(self.bucket_name).upload(file=f, path=bucket_path, file_options={"content-type": "application/json"})
            
        remove(temp_file)
        
        print(f"Dados inseridos no bucket {self.bucket_name} com sucesso.")
        
            
            
            
            
        
        
     

>>>>>>> Stashed changes
def main():
    extract = Extract()
    load = LoadToLakehouse()
    
    data_cliente = extract.get_data("clientes")
    print("Dados do cliente extraídos com sucesso")
    print(f"Quantidade de registros: {len(data_cliente)}")
<<<<<<< Updated upstream
    
    data_produto = extract.get_data("produtos") 
    print("Dados do produto extraídos com sucesso")
    print(f"Quantidade de registros: {len(data_produto)}")
    
    data_pedido = extract.get_data("pedidos")
    print("Dados do pedido extraídos com sucesso")
    print(f"Quantidade de registros: {len(data_pedido)}")

    load.insert_to_bucket_storage(data_cliente, "clientes")
    load.insert_to_bucket_storage(data_produto, "produtos")
    load.insert_to_bucket_storage(data_pedido, "pedidos")
=======
    # data_produto = extract.get_data("produtos") 
    # print("Dados do produto extraídos com sucesso")
    # print(f"Quantidade de registros: {len(data_produto)}")
    # data_pedido = extract.get_data("pedidos")
    # print("Dados do pedido extraídos com sucesso")
    # print(f"Quantidade de registros: {len(data_pedido)}")
    
    
    load.insert_to_bucket_lakehouse(data_cliente, "clientes")
    # load.insert_to_bucket_lakehouse(data_produto, "produtos")
    # load.insert_to_bucket_lakehouse(data_pedido, "pedidos")
    
    print(len(data_cliente))
    
    print("Data inserted successfully")
>>>>>>> Stashed changes
    
    extract.close_connection()
    load.close_connection()
    
    print("Processo finalizado.")


if __name__ == "__main__":
    main()