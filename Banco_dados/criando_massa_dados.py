import uuid

for _ in range(1000):
    with open('teste.sql', 'a+') as file:
        file.write(
f"""
INSERT INTO rodolfoestagiario.tb_pessoa(
                                no_pessoa
                                ,st_ativo
                                ,dh_criacao
                                ,tp_operacao
                                ,nu_versao
                                ,co_uuid
                                ,co_uuid_1
                                ,no_social_pessoa
                                )
                        values(
                                'RODOLFO DE ARAUJO RITZ'
                                ,TRUE
                                ,now()
                                ,'CREATE'
                                ,1
                                ,'{uuid.uuid4()}'
                                ,'32a41f6e-454d-428b-850d-e9e7d269b560'
                                ,'ROD'
                                );
"""            
            )
        
for i in range(1000):
    with open('testess.sql', 'a+') as file:
        file.write(
        f"""
        UPDATE rodolfoestagiario.tb_pessoa
        SET co_seq_pessoa = (co_seq_pessoa - 1000)
        WHERE co_seq_pessoa = 502 ;
        """            
            )