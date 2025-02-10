from dotenv import load_dotenv
from os import getenv, path, remove
from supabase import create_client
import math

class LakehouseConnection():
    def __init__(self):
        load_dotenv()
        self.url = getenv("LAKEHOUSE_URL")
        self.key = getenv("LAKEHOUSE_KEY")
        self.client = create_client(self.url, self.key)
        self.bucket = getenv("BUCKET_NAME")
        self.temp = "./temp"
        self.batch_size = 10_000
        
    def clear_temp(self, *args):
        for file in args:
            if path.exists(file):
                remove(file)

    def close_connection(self):
        self.client = None
    
    def get_data_from_bucket(self, file_name):      
        paths = []
        sub_paths = []
        
        response_paths = self.client.storage.from_(self.bucket).list()
        
        for file in response_paths:
            if file["name"] == ".emptyFolderPlaceholder":
                continue
            paths.append(file["name"])
        
        response_sub_paths = self.client.storage.from_(self.bucket).list(path=paths[0])
        
        for file in response_sub_paths:
            sub_paths.append(file["name"])
        
        recent_path = self.__get_path_recent(paths)
        recent_sub_path = self.__get_path_recent(sub_paths)
        
        file_path_bucket = f"{recent_path}/{recent_sub_path}/{file_name}.parquet"
        temp_path = f"{self.temp}/{file_name}.parquet"
            
        with open(temp_path, "wb+") as f:
            response = self.client.storage.from_(self.bucket).download(file_path_bucket)
            f.write(response)
            
        return temp_path
        
    def __get_path_recent(self, paths):
        path_recent = paths[0]
        
        for path in paths:
            if int(path) > int(path_recent):
                path_recent = path
                
        return path_recent
        
        
    def insert_data_to_lakehouse(self, df, table_name, schema):
        total_rows = df.shape[0]
        
        if total_rows == 0:
            print(f"Não há dados para inserir na tabela {table_name}")
            return
        
        total_batches = math.ceil(total_rows / self.batch_size)
        
        print(f"Inserindo dados na tabela {table_name}, um total de {total_rows} registros serão inseridos em {total_batches} lotes.")
        
        for i in range(0, total_rows, self.batch_size):
            batch_data = df.iloc[i:i + self.batch_size].to_dict(orient="records")
            
            try:
                self.client.schema(schema).table(table_name).insert(batch_data).execute()
                print(f"Inserindo dados na tabela {table_name} - {i + len(batch_data)} registros inseridos.")
            except Exception as e:
                print(f"Erro ao inserir dados na tabela {table_name}")
                print(e)
                break
            
        print(f"Sucesso ao inserir os dados na tabela: {table_name}")
