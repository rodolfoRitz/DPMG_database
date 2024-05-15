from sqlalchemy import Column, String, BigInteger

from Auditavel import Auditavel


class PessoaProcesso(Auditavel):
    """
    Classe que representa a relação entre CPF e Processo\n
    Autor: Pedro Henrique Gonçalves Pires\n
    Data: 08/05/2023 -> 09/08/2023\n
    """
    __tablename__ = 'tb_assistido_processo'
    __table_args__ = {'schema': 'assistidoprocesso'}

    id: Column = Column('co_seq_assistido_processo', BigInteger, primary_key=True)
    uuid_pessoa: Column = Column('co_uuid_2', String(255))
    processo: Column = Column('nu_processo', String(255))

    def get_unique_identifier(self) -> str:
        """
        Retorna um identificador único
        :return: identificadores único
        """

        return f'{self.uuid_pessoa}_{self.processo}'
