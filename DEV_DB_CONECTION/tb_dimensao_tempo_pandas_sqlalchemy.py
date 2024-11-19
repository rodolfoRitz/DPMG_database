import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Configurações do banco de dados PostgreSQL
DATABASE_URL = 'postgresql+psycopg2://postgres:dpmg2022@10.100.64.55:5432/bohr'
engine = create_engine(DATABASE_URL)

# Função para traduzir o dia da semana para português
def traduzir_dia_semana(dia_semana):
    dias = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    return dias[dia_semana]

# Função para traduzir o nome do mês para português
def traduzir_mes(mes):
    meses = {
        "January": "Janeiro",
        "February": "Fevereiro",
        "March": "Março",
        "April": "Abril",
        "May": "Maio",
        "June": "Junho",
        "July": "Julho",
        "August": "Agosto",
        "September": "Setembro",
        "October": "Outubro",
        "November": "Novembro",
        "December": "Dezembro"
    }
    return meses[mes]

# Função para gerar datas em um DataFrame
def gerar_datas_iniciais():
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2050, 12, 31)
    delta = timedelta(days=1)

    # Listas para armazenar os dados
    datas = []
    dias = []
    meses = []
    anos = []
    dias_da_semana = []
    dias_do_mes = []
    trimestres = []
    semestres = []
    nomes_meses = []
    nomes_dias_semana = []

    while start_date <= end_date:
        dia = start_date.day
        mes = start_date.month
        ano = start_date.year
        dia_da_semana_ingles = start_date.strftime('%A')
        nome_mes_ingles = start_date.strftime('%B')

        # Traduzir para português
        dia_da_semana = traduzir_dia_semana(dia_da_semana_ingles)
        nome_mes = traduzir_mes(nome_mes_ingles)

        trimestre = (mes - 1) // 3 + 1
        semestre = 1 if mes <= 6 else 2

        # Adicionar os dados às listas
        datas.append(start_date.date())
        dias.append(dia)
        meses.append(mes)
        anos.append(ano)
        dias_da_semana.append(dia_da_semana)
        dias_do_mes.append(dia)
        trimestres.append(trimestre)
        semestres.append(semestre)
        nomes_meses.append(nome_mes)
        nomes_dias_semana.append(dia_da_semana)

        start_date += delta

    # Criar o DataFrame
    df = pd.DataFrame({
        'data': datas,
        'dia': dias,
        'mes': meses,
        'ano': anos,
        'dia_da_semana': dias_da_semana,
        'dia_do_mes': dias_do_mes,
        'feriado': [False] * len(datas),  # Inicialmente nenhum feriado
        'nome_feriado': [None] * len(datas),  # Nome do feriado inicialmente None
        'trimestre': trimestres,
        'semestre': semestres,
        'nome_mes': nomes_meses,
        'nome_dia_semana': nomes_dias_semana
    })

    return df

# Função para buscar feriados da API Nager.Date
def obter_feriados(ano, pais="BR"):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/{pais}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Função para marcar os feriados e seus nomes no DataFrame
def marcar_feriados(df):
    for ano in range(1900, 3001):
        feriados = obter_feriados(ano)
        for feriado in feriados:
            data_feriado = datetime.strptime(feriado['date'], '%Y-%m-%d').date()
            nome_feriado = feriado['localName']

            # Localizar as linhas no DataFrame que correspondem à data do feriado
            df.loc[df['data'] == data_feriado, 'feriado'] = True
            df.loc[df['data'] == data_feriado, 'nome_feriado'] = nome_feriado

    return df

# Inserir o DataFrame no banco de dados PostgreSQL
def inserir_no_banco(df):
    # Usando 'append' para garantir que a tabela existente não seja recriada, e dados sejam adicionados
    df.to_sql('tb_dimensao_tempo', engine, if_exists='append', index=False)

# Chamar as funções para gerar dados, marcar feriados e inserir no banco
if __name__ == "__main__":
    # Gerar o DataFrame com os dados iniciais
    df_datas = gerar_datas_iniciais()

    # Marcar os feriados no DataFrame
    df_com_feriados = marcar_feriados(df_datas)

    # Inserir os dados no banco de dados PostgreSQL
    inserir_no_banco(df_com_feriados)
