import os
import psycopg2
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('./DEV_DB_CONECTION/environment.env')

# Configurações de conexão usando variáveis de ambiente
conn_params = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': 'postgres'  # Conecte-se ao banco de dados padrão 'postgres'
}

# Função para buscar todos os bancos de dados
def get_databases():
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname;")
        databases = [db[0] for db in cursor.fetchall()]
        cursor.close()
        conn.close()
        return databases
    except Exception as e:
        print(f"Error fetching databases: {e}")
        return []

# Função para buscar esquemas de um banco de dados
def get_schemas(dbname):
    try:
        conn = psycopg2.connect(dbname=dbname, **conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT nspname FROM pg_catalog.pg_namespace WHERE nspname NOT IN ('pg_catalog', 'information_schema') ORDER BY nspname;")
        schemas = [schema[0] for schema in cursor.fetchall()]
        cursor.close()
        conn.close()
        return schemas
    except Exception as e:
        print(f"Error fetching schemas for {dbname}: {e}")
        return []

# Função para buscar tabelas de um esquema
def get_tables(dbname, schema):
    try:
        conn = psycopg2.connect(dbname=dbname, **conn_params)
        cursor = conn.cursor()
        cursor.execute(f"SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = '{schema}' ORDER BY tablename;")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        print(f"Error fetching tables for {schema} in {dbname}: {e}")
        return []

# Função de atualização ao selecionar um banco de dados
def on_database_select(event):
    dbname = database_var.get()
    schemas = get_schemas(dbname)
    schema_var.set('')  # Limpar a seleção do esquema
    schema_list['values'] = schemas
    table_var.set('')  # Limpar a seleção da tabela
    table_list['values'] = []

# Função de atualização ao selecionar um esquema
def on_schema_select(event):
    dbname = database_var.get()
    schema = schema_var.get()
    tables = get_tables(dbname, schema)
    table_var.set('')  # Limpar a seleção da tabela
    table_list['values'] = tables

# Criar a interface gráfica
app = tk.Tk()
app.title("Select Database, Schema, and Table")

# Variáveis para armazenar as seleções
database_var = tk.StringVar()
schema_var = tk.StringVar()
table_var = tk.StringVar()

# Widgets de seleção
tk.Label(app, text="Select Database:").pack(pady=5)
database_list = ttk.Combobox(app, textvariable=database_var)
database_list['values'] = get_databases()
database_list.bind("<<ComboboxSelected>>", on_database_select)
database_list.pack(pady=5)

tk.Label(app, text="Select Schema:").pack(pady=5)
schema_list = ttk.Combobox(app, textvariable=schema_var)
schema_list.bind("<<ComboboxSelected>>", on_schema_select)
schema_list.pack(pady=5)

tk.Label(app, text="Select Table:").pack(pady=5)
table_list = ttk.Combobox(app, textvariable=table_var)
table_list.pack(pady=5)

# Iniciar o loop da interface gráfica
app.mainloop()
