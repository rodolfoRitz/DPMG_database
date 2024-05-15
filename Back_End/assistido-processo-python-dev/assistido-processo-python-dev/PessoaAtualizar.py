import os
from datetime import datetime

import requests
from sqlalchemy import Column, BigInteger, DateTime, String

from Auditavel import Auditavel


class PessoaAtualizar(Auditavel):
    """
    Classe que representa um item da fila de pessoas para atualizar\n
    Autor: Pedro Henrique Gonçalves Pires\n
    Data: 20/06/2023 -> 09/08/2023\n
    """
    __tablename__ = 'tb_controle_atu_processo'
    __table_args__ = {'schema': 'assistidoprocesso'}

    id: Column = Column('co_seq_controle_atu_processo', BigInteger, primary_key=True)
    uuid_pessoa: Column = Column('co_uuid_2', String(255))
    dh_agendamento_atualizacao: Column = Column('dh_agendamento_atualizacao', DateTime)
    dh_ultima_atualizacao: Column = Column('dh_ultima_atualizacao', DateTime)

    def get_documento(self) -> str:
        documentos_pessoa_response = requests.get(f"{os.environ['URL_GERAIS']}documento/service/api/{self.uuid_pessoa}/documentos",
                                                  headers={'Authorization': ''})
        if documentos_pessoa_response.status_code != 200:
            return None

        documentos_pessoa = documentos_pessoa_response.json()

        for documento_pessoa in documentos_pessoa:
            if documento_pessoa.get('tipoDocumento') in ['CPF', 'CNPJ']:
                return documento_pessoa.get('numeroDocumento')

        return None

    def is_pj(self) -> bool:
        documentos_pessoa_response = requests.get(f"{os.environ['URL_GERAIS']}documento/service/api/{self.uuid_pessoa}/documentos",
                                                  headers={'Authorization': ''})
        if documentos_pessoa_response.status_code != 200:
            return None

        documentos_pessoa = documentos_pessoa_response.json()

        for documento_pessoa in documentos_pessoa:
            if documento_pessoa.get('tipoDocumento') == 'CPF':
                return False
            elif documento_pessoa.get('tipoDocumento') == 'CNPJ':
                return True

        return None

    def is_in_the_atualizacao_line(self) -> bool:
        # Se não foi agendada atualização
        if self.dh_agendamento_atualizacao is None:
            return False

        # Se foi agendada atualização e não foi atualizado
        if self.dh_ultima_atualizacao is None:
            return True

        # Verifica se o agendamento é posterior a última atualização
        return self.dh_agendamento_atualizacao > self.dh_ultima_atualizacao

    def set_atualizacao_date(self):
        self.dh_ultima_atualizacao = datetime.now()
