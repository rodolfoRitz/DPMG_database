# https://www.youtube.com/watch?v=m1TYpvIYm74 Vídeo sobre AMBIENTE VIRTUAL

# https://www.canva.com/design/DAFzC5CulD8/04iwNi332-WTnLZhA--Yxw/edit?utm_content=DAFzC5CulD8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
# TinyDB, Streamlit, ...

from tinydb import TinyDB

db = TinyDB('./database.json', indent=2)

document = {'name': 'Rodolfo', 'altura': 1.77}

db.insert(document)

table_produtos = db.table('produtos') # Podemos atribuir a tabela a uma variável

produto1 = {'nome': 'Notebook', 'preco': 3999.90, 'processador': 'Intel Core 15', 'ram_gb': 8}
produto2 = {'nome': 'Geladeira', 'preco': 4500.9, 'processador': 'Intel Core 15', 'ram_gb': 8}