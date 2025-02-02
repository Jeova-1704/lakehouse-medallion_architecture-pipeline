pandas, lakehouse, supabase, dashboard, disponibilizar os dados em uma api, arquitetura medalhão(bronze, silver, gold), pipeline Prefect

Vamos criar um projeto de ponta a ponta, desde a extração dos dados até a disponibilização de um dashboard e uma API para acessar os dados. Vamos usar o pandas para extrair os dados do supabase e subir em nosso data lakehouse (vou suar o supabase para simular pois é uma opção gratuita), vamos usar a arquitetura medalhão(bronze, silver, gold) e o Prefect para criar um pipeline de dados.

Os dados que vamos usar já estão disponíveis no supabase, são dados de uma loja fictícia que vende produtos e tem clientese e pedidos. Vamos fazer a extração, carregar em nosso data lakehouse, limpar e transformar os dados, criar um dashboard para visualização e disponibilizar os dados em uma API.

vamos começar criando a arquitetura medalhão no supabase.

Como Estruturar a Arquitetura Medalhão no Supabase?
No Supabase, vamos organizar a Arquitetura Medalhão criando três esquemas diferentes para armazenar os dados em diferentes níveis de processamento:

📂 Esquema bronze → Dados brutos extraídos
📂 Esquema silver → Dados limpos e transformados
📂 Esquema gold → Dados agregados e prontos para análise

Essa separação mantém os dados organizados e facilita a governança.

Antes de tudo vamos criar uma organização no supabase e um projeto, nesse projeto vamos acessar a parte de SQL Editor e criar os esquemas bronze, silver e gold.

1️⃣ Criando os Esquemas no Supabase
Acesse o SQL Editor no Supabase e execute:
```sql
-- Criar os esquemas para a arquitetura medalhão
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
```
Isso criará três áreas separadas para armazenar os dados de forma organizada.

Agora vamos criar as nossas tabelas no schema bronze primeiro para realizar a extração dos dados e jogar lá:
```sql
CREATE SEQUENCE process_id_seq START 1;

CREATE TABLE bronze.clientes (
    id_cliente TEXT PRIMARY KEY,
    nome TEXT,
    email TEXT,
    telefone TEXT,
    cidade TEXT,
    idade TEXT,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Coluna para a hora do carregamento
    process_id TEXT DEFAULT 'abc' || nextval('process_id_seq')::TEXT
    row_version INT DEFAULT 1  -- Controle de versão do registro (caso haja alterações futuras)
);

CREATE TABLE bronze.produtos (
    id_produto TEXT PRIMARY KEY,
    nome_produto TEXT,
    categoria TEXT,
    preco TEXT,
    estoque TEXT,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Coluna para a hora do carregamento
    process_id TEXT DEFAULT 'abc' || nextval('process_id_seq')::TEXT
    row_version INT DEFAULT 1  -- Controle de versão do registro (caso haja alterações futuras)
);

CREATE TABLE bronze.pedidos (
    id_pedido TEXT PRIMARY KEY,
    id_cliente TEXT REFERENCES bronze.clientes(id_cliente),
    id_produto TEXT REFERENCES bronze.produtos(id_produto),
    quantidade TEXT,
    status TEXT,
    valor_total TEXT,
    data_pedido TEXT,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Coluna para a hora do carregamento
    process_id TEXT DEFAULT 'abc' || nextval('process_id_seq')::TEXT
    row_version INT DEFAULT 1  -- Controle de versão do registro (caso haja alterações futuras)
);
```
