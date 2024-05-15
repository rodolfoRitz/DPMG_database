from tinydb import TinyDB


db = TinyDB('./database.json', indent=2)

while True:
    pessoa = {
        'nome': input('Digite o nome da pessoa: '),
        'altura': float(input('Digite a altura da pessoa: '))
    }

    profissao = input('Digiite sua profissão: ')
    pessoa['profissao'] = profissao if profissao != '' else None

    resp = input('Deseja continuar? [S/N]')
    if resp.upper() == 'N':
        break

    db.table('pessoas').insert(pessoa)