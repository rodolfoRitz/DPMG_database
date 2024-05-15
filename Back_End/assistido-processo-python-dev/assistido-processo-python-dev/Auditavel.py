from sqlalchemy import Column, String, Boolean, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Auditavel(Base):
    __abstract__ = True

    projeto_modificador = Column('sg_projeto_modificador', String(15))
    acao_modificadora = Column('sg_acao_modificadora', String(15))
    end_point_modificador = Column('no_end_point_modificador', String(255))
    ativo = Column('st_ativo', Boolean, default=True)
    data_criacao = Column('dh_criacao', DateTime, default=func.now())
    data_alteracao = Column('dh_alteracao', DateTime, onupdate=func.now())
    operacao = Column('tp_operacao', String(255), default='CREATE', onupdate='UPDATE')
    versao = Column('nu_versao', Integer, default=1)
    uuid = Column('co_uuid', String(255), default=func.uuid_generate_v4())
    uuid_usuario_modificador = Column('co_uuid_1', String(255))

    def set_audit_fields(self, projeto_modificador: str, acao_modificadora: str, end_point_modificador: str, uuid_usuario_modificador: str):
        self.projeto_modificador = projeto_modificador
        self.acao_modificadora = acao_modificadora
        self.end_point_modificador = end_point_modificador
        self.uuid_usuario_modificador = uuid_usuario_modificador
        self.versao = (self.versao + 1) if (self.versao is not None) else 1
