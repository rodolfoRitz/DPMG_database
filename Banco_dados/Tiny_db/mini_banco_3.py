from tinydb import TinyDB, Query

def mostrar_pessoas(pessoas: list[dict]):
    for index, pessoa in enumerate(pessoas, start=1):
        print(f'------ {index}º -----')
        print(f'Nome: {pessoa["nome"]}')
        print(f'Altura: {pessoa["altura"]}')
        print(f'Profissão: {pessoa["profissao"]}')
        print('----------------')

db = TinyDB('./database.json', indent=2)
t_pessoas = db.table('pessoas')

pessoas = t_pessoas.all()
#print(todas_pessoas)

Pessoa = Query()

pessoas = t_pessoas.search(Pessoa.altura < 1.65)
#desenvolvedores = t_pessoas.search(Pessoa.profissao = 'Desenvolvedor')

# Exemplos
'''
db.table('produtos').search(Produto.preco < 4000)
db.table('produtos').search(Produto['name'] < 4000)
'''

'''print(desenvolvedores)
mostrar_pessoas(desenvolvedores)'''