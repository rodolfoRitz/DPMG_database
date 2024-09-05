from pymongo import MongoClient
import pymysql

# Conectar ao MongoDB
client_mongo = MongoClient('localhost', 27017)
# Seleciona na variável 'db' o Database chamado 'People'
db_mongo = client_mongo.People
# Obtendo os dados da coleção "info"
dados_info_mongo = db_mongo.info.find()


# Conectar ao MySQL (Porta:3306)
connection_mysql = pymysql.connect(
    host='localhost 2',
    user='root@172.17.0.1',
    password='123',
    database='mongo_db_data'
)
cursor_mysql = connection_mysql.cursor()

# Criar uma tabela no MySQL se não existir
# create_table_query = '''CREATE TABLE IF NOT EXISTS tb_pessoa (nome VARCHAR(255))'''
# cursor_mysql.execute(create_table_query)
##################################################
# {
#   "_id": {
#     "$oid": "664b832fc80cf0ac939a0f11"
#   },
#   "nome": "Tara Price",
#   "sexo": "M",
#   "cartao_de_credito": {
#     "numero": "6569627117803551",
#     "cvv": "764",
#     "validade": "01/26"
#   },
#   "mae": "Linda Chandler",
#   "senha": "&%2AZzbxta",
#   "documentos": {
#     "rg": "583190350 SSP RJ",
#     "cpf": "41268251267"
#   },
#   "sangue": "O+",
#   "emprego": "Accountant, chartered certified",
#   "nascimento": "18/06/1936",
#   "telefone": "+1-301-685-8874",
#   "endereco": {
#     "cidade": "West Elizabeth",
#     "uf": "WA",
#     "logradouro": "000 Alejandro Locks",
#     "cep": "03203"
#   },
#   "email": "rebecca20@example.org",
#   "peso": "99.23 kg",
#   "altura": "1.73 m"
# }

# Inserir dados do MongoDB no MySQL
for dado in dados_info_mongo:
    id            = dado.get('_id', '') # Ou "$oid"
    nome          = dado.get('nome', '')
    sexo          = dado.get('sexo', '')
    numero        = dado.get('numero', '')
    cvv           = dado.get('cvv', '')
    validade      = dado.get('validade', '')
    mae           = dado.get('mae', '')
    senha         = dado.get('senha', '')
    documento_rg  = dado.get('rg', '')
    documento_cpf = dado.get('cpf', '')
    sangue        = dado.get('sangue', '')
    emprego       = dado.get('emprego', '')
    nascimento    = dado.get('nascimento', '')
    telefone      = dado.get('telefone', '')
    cidade        = dado.get('cidade', '')
    uf            = dado.get('uf', '')
    logradouro    = dado.get('logradouro', '')
    cep           = dado.get('cep', '')
    email         = dado.get('email', '')
    peso          = dado.get('peso', '')
    altura        = dado.get('altura', '')

    # Inserir na tabela tb_pessoa
    insert_query = "INSERT INTO tb_pessoa (co_seq_pessoa, no_da_pessoa, tp_sexo) VALUES (%s, %s)"
    cursor_mysql.execute(insert_query, (id, nome, sexo))
    connection_mysql.commit()
    # `co_seq_pessoa` INT AUTO_INCREMENT PRIMARY KEY, sera que ele deve ser inserido junto com todos os outros dados ou será automático e nem preciso ser citado  no INSERT?
    # Na verdade o 'co_seq_pessoa' não deveria estar no auto_increment, pois o ID já existe e o dado pode ser exportado.

    # Inserir na tabela tb_cartao_credito
    insert_query = "INSERT INTO tb_cartao_credito (co_pessoa, nu_cartao_credito, nu_cvv, dt_validade) VALUES (%s, %s, %s, %s)"
    cursor_mysql.execute(insert_query, (id, numero, cvv, validade))
    connection_mysql.commit()
    #   `dt_validade` date DEFAULT NULL, TROCAR PARA VARCHAR

    # Inserir na tabela tb_documento
    insert_query = "INSERT INTO tb_documento (co_pessoa, nu_documento, tp_documento) VALUES (%s, %s, %s)"
    cursor_mysql.execute(insert_query, (id, documento_rg, documento_cpf))
    connection_mysql.commit()
    # O certo seria colocar os dois dados em colunas diferentes. Pois o 'tp_documento' neste caso não funciona imediatamente. Adicionar o tp após importação.

    # Inserir na tabela tb_geral_pessoa
    insert_query = "INSERT INTO tb_geral_pessoa (co_pessoa, dt_nasc, tp_sangue, no_profissao, nu_peso, nu_altura, ds_senha) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor_mysql.execute(insert_query, (id, nascimento, sangue, emprego, peso, altura, senha))
    connection_mysql.commit()

    # Inserir na tabela tb_endereco
    insert_query = "INSERT INTO tb_endereco (co_pessoa, no_cidade, no_municipio, no_logradouro, nu_cep) VALUES (%s, %s, %s, %s, %s)"
    cursor_mysql.execute(insert_query, (id, cidade, uf, logradouro, cep))
    connection_mysql.commit()

    # Inserir na tabela tb_filiacao_pessoa
    insert_query = "INSERT INTO tb_filiacao_pessoa (co_pessoa, no_filiacao) VALUES (%s, %s)"
    cursor_mysql.execute(insert_query, (id, mae))
    connection_mysql.commit()

    # Inserir na tabela tb_email
    insert_query = "INSERT INTO tb_email (co_pessoa, no_email) VALUES (%s, %s)"
    cursor_mysql.execute(insert_query, (id, email))
    connection_mysql.commit()

    # Inserir na tabela tb_telefone
    insert_query = "INSERT INTO tb_telefone (co_pessoa, nu_telefone) VALUES (%s, %s)"
    cursor_mysql.execute(insert_query, (id, telefone))
    connection_mysql.commit()

# Fechar conexões
cursor_mysql.close()
connection_mysql.close()
client_mongo.close()
