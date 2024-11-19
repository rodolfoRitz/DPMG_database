import requests
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta

# Configurações do banco de dados PostgreSQL
DATABASE_URL = 'postgresql+psycopg2://postgres:dpmg2022@10.100.64.55:5432/bohr'

# Conexão com o banco de dados usando SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definição da tabela tb_dimensao_tempo
class DimensaoTempo(Base):
    __tablename__ = 'tb_feriados_2'
    
    id_tempo = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, unique=True, nullable=False)
    dia = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    dia_da_semana = Column(String, nullable=False)
    dia_do_mes = Column(Integer, nullable=False)
    feriado = Column(Boolean, default=False)
    nome_feriado = Column(String, nullable=True)  # Nova coluna para o nome do feriado
    trimestre = Column(Integer, nullable=False)
    semestre = Column(Integer, nullable=False)
    nome_mes = Column(String, nullable=False)
    nome_dia_semana = Column(String, nullable=False)

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

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

# Função para popular a tabela com as datas
def gerar_datas_iniciais():
    start_date = datetime(1900, 1, 1)
    end_date = datetime(3000, 12, 31)
    delta = timedelta(days=1)
    
    while start_date <= end_date:
        dia = start_date.day
        mes = start_date.month
        ano = start_date.year
        dia_da_semana_ingles = start_date.strftime('%A')  # Nome do dia da semana (ex: Monday)
        nome_mes_ingles = start_date.strftime('%B')       # Nome do mês (ex: January)
        
        # Traduzir os nomes para português
        dia_da_semana = traduzir_dia_semana(dia_da_semana_ingles)
        nome_mes = traduzir_mes(nome_mes_ingles)
        
        trimestre = (mes - 1) // 3 + 1  # Calcula o trimestre
        semestre = 1 if mes <= 6 else 2  # Calcula o semestre
        
        dimensao_tempo = DimensaoTempo(
            data=start_date.date(),
            dia=dia,
            mes=mes,
            ano=ano,
            dia_da_semana=dia_da_semana,
            dia_do_mes=dia,
            trimestre=trimestre,
            semestre=semestre,
            nome_mes=nome_mes,
            nome_dia_semana=dia_da_semana
        )
        
        session.add(dimensao_tempo)
        start_date += delta
    
    session.commit()

# Função para buscar feriados da API Nager.Date
def obter_feriados(ano, pais="BR"):
    url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/{pais}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Função para marcar os feriados na tabela e adicionar o nome do feriado
def marcar_feriados():
    for ano in range(2000, 2050):
        feriados = obter_feriados(ano)
        for feriado in feriados:
            data_feriado = datetime.strptime(feriado['date'], '%Y-%m-%d').date()
            nome_feriado = feriado['localName']  # Nome do feriado
            # Atualizar a coluna 'feriado' para True e definir o nome do feriado
            session.query(DimensaoTempo).filter(DimensaoTempo.data == data_feriado).update({
                "feriado": True,
                "nome_feriado": nome_feriado
            })
        session.commit()

# Chamar a função para gerar datas e marcar feriados
if __name__ == "__main__":
    gerar_datas_iniciais()
    marcar_feriados()
