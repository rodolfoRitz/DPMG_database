'''
Este é um código para criação de Classes, através do método construtor '__init__' que pode conter vários atributos e suas funções.
'''

class Pessoa:
    def __init__(self, nome: str, altura: float, idade: int) -> None: # Método construtor.
        self.nome = nome
        self.altura = altura
        self.idade = idade
    
pessoa_1 = Pessoa('Pedro', 1.72, 19)
#print(type(pessoa_1)) # class '__main__' faz oq? class '__main__.Pessoa'
#print(f"{pessoa_1.nome} - {pessoa_1.altura} - {pessoa_1.idade}") #end= '-'
#print(vars(pessoa_1)) #O método 'vars' retorna um dicionário com os atributos e seus respectivos valores do objeto. 

def mostrar_idade():
    print(pessoa_1.idade)

def somar_um_ano(self):
    self.idade += 1

#mostrar_idade()
#somar_um_ano(pessoa_1)
#mostrar_idade()

class Fatura:
    def __init__(self, nome:str, preco_item: float, quantidade_item: int): #valor_total_fatura: float
        self.nome = nome
        self.preco_item = preco_item
        self.quantidade_item = quantidade_item
        #self.valor_total_fatura = valor_total_fatura

fatura_1 = Fatura('cemig', 1.99, 3)
'''
def new_fatura(new_nome, ):
    new_nome = input('Digite o nome da fatura: ')
    ...
'''

def gerar_fatura(quantidade_item: int, preco_item: float) -> float:
    valor_fatura = quantidade_item * preco_item
    print(valor_fatura)

#print(vars(fatura_1))
#gerar_fatura(3, 1.99)

class Carro:
    def __init__(self, nome:str, marca:str, ano:int, cor='Preto'): # Ao definir um padrão para a variável, deve-se usar o '='.
        self.nome = nome
        self.marca = marca
        self.ano = ano
        self.cor = cor

carro_1 = Carro('Fusca', 'Volkswagen', 1976)
#print(vars(carro_1))

class Bola:
    def __init__(self, cor:str, circunferencia:float, material:str):
        self.cor = cor
        self.circunferencia = circunferencia
        self.material = material

    def troca_cor(self, nova_cor:str) -> str:
        self.cor = nova_cor
    
    def mostra_cor(self):
        print(self.cor)

'''
bola_1 = Bola('branca', 2.8, 'ferro')
bola_1.mostra_cor()
bola_1.troca_cor('azuli')
bola_1.mostra_cor()
'''

class Quadrado:
    def __init__(self, tamanho_lado:float):
        self.tamanho_lado = tamanho_lado
    
    def mudar_valor_lado(self, novo_valor):
        self.tamanho_lado = novo_valor
    
    def retornar_valor_lado(self):
        print(self.tamanho_lado)

    def calcular_area(self):
        valor_area = 0
        self.tamanho_lado = valor_area
        valor_area_calculado = valor_area * valor_area
        print(valor_area_calculado)
        
quadrado_1 = 4
quadrado_1.calcular_area()