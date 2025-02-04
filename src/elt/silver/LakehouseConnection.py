from dotenv import load_dotenv
from os import getenv
from supabase import create_client
import math

class LakehouseConnection():
    def __init__(self):
        load_dotenv()
        self.url = getenv("LAKEHOUSE_URL")
        self.key = getenv("LAKEHOUSE_KEY")
        self.client = create_client(self.url, self.key)
        self.batch_size = 10_000

    def close_connection(self):
        self.client = None
        
    def get_data_from_lakehouse(self, table_name, schema):
        all_data = []
        offset = 0
        
        while True:
            try:
                response = self.client.schema(schema).table(table_name).select("*").range(offset, offset + self.batch_size - 1).execute()
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
