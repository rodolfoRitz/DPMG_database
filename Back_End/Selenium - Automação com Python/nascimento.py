import random

class nascimento:
    @staticmethod
    def gerar_data_nascimento_aleatoria():
        rand = random.Random()

        # Dia entre 1 e 31
        dia = rand.randint(1, 31)

        # Mês entre 1 e 12
        mes = rand.randint(1, 12)

        # Ano entre 1980 e 2023
        ano = rand.randint(1980, 2023)

        return "{:02d}/{:02d}/{:04d}".format(dia, mes, ano)
