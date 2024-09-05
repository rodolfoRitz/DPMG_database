from pymongo import MongoClient
import pymysql.cursors
#import pymysql

# Conectar ao MongoDB
client_mongo = MongoClient('localhost', 27017)
# Seleciona na variável 'db' o Database chamado 'People'
db_mongo = client_mongo.People
# Obtendo os dados da coleção "info"
dados_info_mongo = db_mongo.info.find()


# Conectar ao MySQL (Porta:3306)
connection_mysql = pymysql.connect(
    host='localhost2',
    user='root@172.17.0.1',
    password='123',
    database='mongo_db_data'
)
cursor_mysql = connection_mysql.cursor()

connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             database='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)

# Fechar conexões
cursor_mysql.close()
connection_mysql.close()
client_mongo.close()
