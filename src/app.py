import subprocess

def run_elt_schema_bronze():
    print("Iniciando processo de extração de dados e carga na camada bronze.")
    subprocess.run(["python", "src/elt/bronze/main.py"])
    print("Processo de extração de dados e carga na camada bronze finalizado.")

def run_elt_schema_silver():
    print("Iniciando processo de transformação de dados e carga na camada silver.")
    subprocess.run(["python", "src/elt/silver/main.py"])
    print("Processo de transformação de dados e carga na camada silver finalizado.")
    

if __name__ == "__main__":
    run_elt_schema_bronze()
    run_elt_schema_silver()
    