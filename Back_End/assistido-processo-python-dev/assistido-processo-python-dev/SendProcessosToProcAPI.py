import os
import re
from threading import Thread

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from PessoaProcesso import PessoaProcesso
from data_sets.Logger import Logger

success_log_file = os.path.join('log_send_processos_procapi', 'success.log')
success_logger = Logger('success', success_log_file)
details_logger = Logger('details', os.path.join('log_send_processos_procapi', 'details.log'))
errors_logger = Logger('errors', os.path.join('log_send_processos_procapi', 'errors.log'))


def create_db_session():
    engine = create_engine(
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}",
        pool_pre_ping=True
    )
    Session = sessionmaker(bind=engine)
    session: Session = Session()

    return session


def get_processos_success_log() -> list[str]:
    """
    Get the Processos that are not in the Succes Log
    :return: Processos that are in the Succes Log
    """
    if not os.path.exists(success_log_file):
        return []

    # Read the content of the succes log file
    with open(success_log_file, 'r') as file:
        success_log_content = file.read()

    # Define the regular expression for the Processo
    processo_pattern = r'Processo\s+(\d{20})'

    # Get the CPFs and CNPJs from the succes log
    details_logger.log(f"Getting the Processos from the succes log: {success_log_file}...", to_print=True)
    processos = re.findall(processo_pattern, success_log_content)
    details_logger.log("Got the Processos from the succes log!")

    return processos  # Retorna os Processos no log de sucesso


def select_pessoas_processos_numeros(session, processos_to_remove: list[str] = []) -> list[str]:
    """
    Get all Processos from PessoaProcesso Table
    :return: List of Processos
    """
    if len(processos_to_remove) == 0:
        processsos_row = session.query(PessoaProcesso.processo).all()
    else:
        processsos_row = session.query(PessoaProcesso.processo).filter(
            PessoaProcesso.processo.not_in(processos_to_remove)
        ).all()

    processos_number = []
    for processo_row in processsos_row:
        processos_number.append(processo_row[0])

    return processos_number


def send_processos_to_procapi(processos: list[str], thread_number: int = -1) -> None:
    """
    Send Processos to ProcAPI
    :param processos: Processos to send
    :return: None
    """
    # Verifica se é uma lista
    if not isinstance(processos, list):
        processos = [processos]

    # Verifica se tem algo para enviar
    if len(processos) == 0:
        return

    headers: dict[str, str] = {
        "Accept": "application/json",
        'Authorization': f"Token {os.environ['TOKEN_PROCAPI']}"
    }

    # Envia cada processo para o ProcAPI
    for index, processo in enumerate(processos):
        # Envia o processo
        response = requests.get(f"{os.environ['URL_PROCAPI']}processos/{processo}/", headers=headers)

        # Verifica se deu erro
        if response.status_code != 200:
            errors_logger.log(f"Thr{thread_number} - {index} - Error sending Processo {processo} to ProcAPI: {response.text}", to_warn=True)
        else:
            success_logger.log(f"Thr{thread_number} - {index} - Processo {processo} sent to ProcAPI", to_print=True)


def send_processos_from_postgresql_to_procapi(thread_quantity: int = 8):
    """
    Send Processos from PostgreSQL to ProcAPI
    :return: None
    """
    # Cria a sessão
    session = create_db_session()

    # Seleciona todos os processos
    processos_already_sent = get_processos_success_log()
    processos = select_pessoas_processos_numeros(session, processos_already_sent)

    # Cria os grupos de processos
    processos_groups = []
    for i in range(thread_quantity):
        processos_groups.append([])

    # Manda os processos para os grupos
    for index, processo in enumerate(processos):
        processos_groups[index % thread_quantity].append(processo)

    # Monta as threads
    threads: list[Thread] = []
    for index, processos in enumerate(processos_groups):
        thread = Thread(target=send_processos_to_procapi, args=(processos, index))
        threads.append(thread)

    # Starta as threads
    for thread in threads:
        thread.start()

    # Espera as threads terminarem
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    send_processos_from_postgresql_to_procapi()
