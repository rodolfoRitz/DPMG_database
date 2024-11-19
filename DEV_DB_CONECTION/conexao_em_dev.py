import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# print(f"{os.getenv('DB_NAME')}, {os.getenv('DB_USER')}, {os.getenv('DB_PASSWORD')}, {os.getenv('DB_HOST')}, {os.getenv('DB_PORT')}")

# Carrega variáveis de ambiente do arquivo .env
load_dotenv('./DEV_DB_CONECTION/environment.env')

# Configurações de conexão usando variáveis de ambiente
conn_params = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME')
}

print(f"{os.getenv('DB_NAME')}, {os.getenv('DB_USER')}, {os.getenv('DB_PASSWORD')}, {os.getenv('DB_HOST')}, {os.getenv('DB_PORT')}")

print(conn_params)

# Função para listar esquemas de um banco de dados
def list_schemas(dbname):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), dbname=os.getenv('DB_NAME'))
        conn.autocommit = True  # Necessário para mudar de banco de dados
        cursor = conn.cursor()
        
        # Busca os esquemas
        cursor.execute(sql.SQL("SELECT nspname FROM pg_catalog.pg_namespace WHERE nspname NOT IN ('pg_catalog', 'information_schema') ORDER BY nspname;"))
        
        schemas = cursor.fetchall()
        
        print(f'Schemas in database {dbname}:')
        for schema in schemas:
            print(f'  {schema[0]}')
    
    except Exception as e:
        print(f'Error connecting to database {dbname}: {e}')
    finally:
        # Garantir que o cursor e a conexão sejam fechados
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Conectar ao banco de dados principal para listar todos os bancos
conn = None
cursor = None
try:
    # conn = psycopg2.connect(**conn_params)
    conn = psycopg2.connect(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), dbname=os.getenv('DB_NAME'))
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Consulta para listar todos os bancos de dados
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;")
    
    databases = cursor.fetchall()
    
    for db in databases:
        dbname = db[0]
        list_schemas(dbname)

except Exception as e:
    print(f'Error connecting to the main database: {e}')
finally:
    # Garantir que o cursor e a conexão sejam fechados
    if cursor:
        cursor.close()
    if conn:
        conn.close()
