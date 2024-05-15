import random

class nome:
    def _init_(self):
        pass

    PRIMEIROS_NOMES = [
        "Ana", "Pedro", "Mariana", "Lucas", "Isabela",
        "Gabriel", "Juliana", "Rafael", "Beatriz", "Felipe",
        "Carolina", "Matheus", "Camila", "Vinícius", "Natália",
        "Gustavo", "Amanda", "André", "Larissa", "Diego",
        "Bianca", "Roberto", "Fernanda", "Ricardo", "Monique",
        "Raul", "Thaís", "José", "Patrícia", "Alexandre",
        "Letícia", "Rogério", "Priscila", "Bruno", "Vanessa",
        "Hugo", "Débora", "César", "Marina", "Leandro",
        "Laura", "Marcelo", "Jéssica", "Daniel", "Tatiane",
        "Eduardo", "Raquel", "Luiz", "Sandra"
    ]

    SOBRENOMES = [
        "Silva", "Santos", "Oliveira", "Pereira", "Lima",
        "Ferreira", "Costa", "Rodrigues", "Almeida", "Nascimento",
        "Cunha", "Martins", "Araújo", "Cardoso", "Carvalho",
        "Gomes", "Mendes", "Barbosa", "Rocha", "Pinto",
        "Souza", "Freitas", "Correia", "Dias", "Teixeira",
        "Morais", "Reis", "Sales", "Campos", "Melo",
        "Lopes", "Batista", "Fernandes", "Ribeiro", "Pires",
        "Monteiro", "Lima", "Marques", "Castro", "Sousa",
        "Cruz", "Machado", "Miranda", "Azevedo", "Vieira",
        "Dantas", "Ramos", "Alves", "Farias", "Neves"
    ]

    TERCEIRO_NOME = [
        "Santos", "Oliveira", "Pereira", "Lima", "Ferreira",
        "Costa", "Rodrigues", "Almeida", "Nascimento", "Cunha",
        "Martins", "Araújo", "Cardoso", "Carvalho", "Gomes",
        "Mendes", "Barbosa", "Rocha", "Pinto", "Souza",
        "Freitas", "Correia", "Dias", "Teixeira", "Morais",
        "Reis", "Sales", "Campos", "Melo", "Lopes",
        "Batista", "Fernandes", "Ribeiro", "Pires", "Monteiro",
        "Lima", "Marques", "Castro", "Sousa", "Cruz",
        "Machado", "Miranda", "Azevedo", "Vieira", "Dantas",
        "Ramos", "Alves", "Farias", "Neves"
    ]

    QUARTO_NOME = [
        "Silva", "Santos", "Oliveira", "Pereira", "Lima",
        "Ferreira", "Costa", "Rodrigues", "Almeida", "Nascimento",
        "Cunha", "Martins", "Araújo", "Cardoso", "Carvalho",
        "Gomes", "Mendes", "Barbosa", "Rocha", "Pinto",
        "Souza", "Freitas", "Correia", "Dias", "Teixeira",
        "Morais", "Reis", "Sales", "Campos", "Melo",
        "Lopes", "Batista", "Fernandes", "Ribeiro", "Pires",
        "Monteiro", "Lima", "Marques", "Castro", "Sousa",
        "Cruz", "Machado", "Miranda", "Azevedo", "Vieira",
        "Dantas", "Ramos", "Alves", "Farias", "Neves"
    ]

    QUINTO_NOME = [
        "Pereira", "Lima", "Ferreira", "Costa", "Rodrigues",
        "Almeida", "Nascimento", "Cunha", "Martins", "Araújo",
        "Cardoso", "Carvalho", "Gomes", "Mendes", "Barbosa",
        "Rocha", "Pinto", "Souza", "Freitas", "Correia",
        "Dias", "Teixeira", "Morais", "Reis", "Sales",
        "Campos", "Melo", "Lopes", "Batista", "Fernandes",
        "Ribeiro", "Pires", "Monteiro", "Lima", "Marques",
        "Castro", "Sousa", "Cruz", "Machado", "Miranda",
        "Azevedo", "Vieira", "Dantas", "Ramos", "Alves",
        "Farias", "Neves", "Oliveira", "Silva"
    ]

    nomes_femininos = [
        "Ana", "Mariana", "Isabela", "Juliana", "Beatriz",
        "Carolina", "Camila", "Natália", "Amanda", "Larissa",
        "Bianca", "Fernanda", "Monique", "Letícia", "Gabriela",
        "Thaís", "Patrícia", "Lívia", "Bruna", "Vanessa",
        "Débora", "Marina", "Laura", "Jéssica", "Tatiane",
        "Raquel", "Sandra", "Lívia", "Priscila", "Vanessa",
        "Adriana", "Cristiane", "Carla", "Daniela", "Roberta",
        "Renata", "Luciana", "Valéria", "Flávia", "Aline",
        "Evelyn", "Alice", "Luana", "Vitória", "Eduarda",
        "Clara", "Giovanna", "Fernanda", "Natalia", "Lorena",
        "Julia", "Elisa", "Isabel", "Rafaela", "Bárbara",
        "Renata", "Luciana", "Valéria", "Flávia", "Aline",
        "Evelyn", "Alice", "Luana", "Vitória", "Eduarda",
        "Clara", "Giovanna", "Fernanda", "Natalia", "Lorena",
        "Julia", "Elisa", "Isabel", "Rafaela", "Bárbara",
        "Gabriella", "Helena", "Leticia", "Samanta", "Aurora",
        "Laís", "Elena", "Nathalia", "Isis", "Manuela",
        "Sophia", "Valentina", "Gabrielle", "Laura", "Clara"
    ]

    @staticmethod
    def gerar_nome_aleatorio():
        primeiro_nome = random.choice(nome.PRIMEIROS_NOMES)
        sobrenome = random.choice(nome.SOBRENOMES)
        terceiro_nome = random.choice(nome.TERCEIRO_NOME)
        quarto_nome = random.choice(nome.QUARTO_NOME)
        quinto_nome= random.choice(nome.QUINTO_NOME)
        return f"{primeiro_nome} {sobrenome} {terceiro_nome} {quarto_nome} {quinto_nome}"

    @staticmethod
    def gerar_nome_mae():
        nome_mae=random.choice(nome.nomes_femininos)
        sobrenome_mae = random.choice(nome.SOBRENOMES)
        terceiro_nome_mae = random.choice(nome.TERCEIRO_NOME)
        quarto_nome_mae = random.choice(nome.QUARTO_NOME)
        quinto_nome_mae = random.choice(nome.QUINTO_NOME)
        return f"{nome_mae} {sobrenome_mae} {terceiro_nome_mae} {quarto_nome_mae} {quinto_nome_mae}"
