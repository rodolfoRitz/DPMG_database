import random

class cpf:
    def _init_(self):
        pass

    @staticmethod
    def gerar_cpf_ficticio():
        # Gerar os 9 primeiros dígitos do CPF
        digito1 = random.randint(0, 9)
        digito2 = random.randint(0, 9)
        digito3 = random.randint(0, 9)
        digito4 = random.randint(0, 9)
        digito5 = random.randint(0, 9)
        digito6 = random.randint(0, 9)
        digito7 = random.randint(0, 9)
        digito8 = random.randint(0, 9)
        digito9 = random.randint(0, 9)

        # Calcular o primeiro dígito verificador
        soma1 = digito1 * 10 + digito2 * 9 + digito3 * 8 + digito4 * 7 + digito5 * 6 + digito6 * 5 + digito7 * 4 + digito8 * 3 + digito9 * 2
        resto1 = soma1 % 11
        primeiro_digito_verificador = 0 if resto1 < 2 else 11 - resto1

        # Calcular o segundo dígito verificador
        soma2 = digito1 * 11 + digito2 * 10 + digito3 * 9 + digito4 * 8 + digito5 * 7 + digito6 * 6 + digito7 * 5 + digito8 * 4 + digito9 * 3 + primeiro_digito_verificador * 2
        resto2 = soma2 % 11
        segundo_digito_verificador = 0 if resto2 < 2 else 11 - resto2

        # Formatar o CPF fictício
        cpf_formatado = f"{digito1}{digito2}{digito3}.{digito4}{digito5}{digito6}.{digito7}{digito8}{digito9}-{primeiro_digito_verificador}{segundo_digito_verificador}"

        return cpf_formatado