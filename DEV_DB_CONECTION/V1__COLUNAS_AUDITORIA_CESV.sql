-------------------------------------------------
-- TB_ANEXO e historico
-------------------------------------------------
ALTER TABLE IF EXISTS tb_anexo 
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_anexo 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_anexo 
ALTER COLUMN no_end_point_modificador SET NOT NULL;

ALTER TABLE IF EXISTS th_anexo_hist 
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_anexo_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_anexo_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_anexo_hist
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_anexo_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_anexo_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_AREA e historico
-------------------------------------------------
-- Na TB as colunas de segurança (sg_projeto_modificador,  sg_acao_modificadora, no_end_point_modificador) não estão sendo gravadas em todos os registros.
-- Na TH as colunas de segurança (sg_projeto_modificador,  sg_acao_modificadora, no_end_point_modificador) não estão sendo gravadas em todos os registros.
-- Na TH a dh_fim_hist está gravando o ínicio do registro e não o fim (desativação).

ALTER TABLE IF EXISTS tb_area 
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_area 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_area 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_area 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS tb_area 
ALTER COLUMN co_uuid_1 SET NOT NULL;

ALTER TABLE IF EXISTS th_area_hist 
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_area_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_area_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_area_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_area_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_area_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_CANDIDATURA e historico
-------------------------------------------------
-- A TB não está gravando a versão inicial corretamente, a coluna nu_versao não está alterando quando realiza uma alteração (UPDATE).
-- A TH não está gravando as versões iniciais corretamente, a coluna nu_versao = 1 e a dh_alteracao está sendo gravada.
-- Na TH o tp_operacao é CREATE e o registro tem diversas versões.

ALTER TABLE IF EXISTS tb_candidatura 
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_candidatura 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_candidatura 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_candidatura 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS tb_candidatura 
ALTER COLUMN co_uuid_1 SET NOT NULL;

ALTER TABLE IF EXISTS th_candidatura_hist 
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_candidatura_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_candidatura_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_candidatura_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_candidatura_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_candidatura_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_CATEGORIA e historico
-------------------------------------------------
-- A dh_criacao não está sendo gerada para todos os registros.
-- A TH tem menos dados que a TB, mas eles podem ter sido apagados.

ALTER TABLE IF EXISTS tb_categoria
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_categoria 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_categoria 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_categoria 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS tb_categoria 
ALTER COLUMN co_uuid_1 SET NOT NULL;

ALTER TABLE IF EXISTS th_categoria_hist
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_categoria_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_categoria_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_categoria_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_categoria_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_categoria_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_DILACAO_CANDIDATURA e historico
-------------------------------------------------
-- A dh_alteracao foi preenchida mas o registro não foi alterado.
-- Na TH, o tp_operacao continua CREATE para nu_versao 2 ou acima. 

-------------------------------------------------
-- TB_DOCUMENTO_CANDIDATURA e historico
-------------------------------------------------
-- Na TH a dh_fim_hist está sendo gravada para nu_versao 1 sem o registro ter sido desativado (tp_operacao = DELETE, st_ativo = FALSE, nu_versao > 1)

ALTER TABLE IF EXISTS tb_documento_candidatura
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_documento_candidatura 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_documento_candidatura 
ALTER COLUMN no_end_point_modificador SET NOT NULL;

ALTER TABLE IF EXISTS th_documento_candidatura_hist
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_documento_candidatura_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_documento_candidatura_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_documento_candidatura_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_documento_candidatura_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_ETAPA e historico
-------------------------------------------------
-- Os dados da TB não estão sendo gravados na TH.

-------------------------------------------------
-- TB_ETAPA_PROCES_SELETIVO e historico
-------------------------------------------------
-- Na TH existem registros com nu_versao > 1, tp_operacao = create e sem dh_alteracao, que estao sendo gravados errado.
-- Na TH o registro não havia sido desativado mas possui dh_fim_hist (tp_operacao = DELETE, st_ativo = FALSE, nu_versao > 1).

-------------------------------------------------
-- TB_INSTITUICAO_ENSINO e historico
-------------------------------------------------
-- Na TB os registros NÃO ESTÃO GRAVANDO CORRETAMENTE AS VERSOES POSTERIORES. Possuem tp_operacao = CREATE, nu_versao = 1 e a dh_alteracao preenchida.
-- A TH não está gravando corretamente o tp_operacao, pois alguns registros tem várias versões com tp_operacao = CREATE. O tp_operacao não está mudando. 
-- E na TH tem tp_operacao = UPDATE com nu_versao = 1.
-- Na TH todos os registros estão gravando a dh_alteracao e dh_fim_hist independente da versão, deveria ser somente quando desativado.
-- Na TB a dh_alteracao está sendo gravada de forma errada em alguns registros.

ALTER TABLE IF EXISTS tb_instituicao_ensino
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_instituicao_ensino 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_instituicao_ensino 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_instituicao_ensino 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS tb_instituicao_ensino 
ALTER COLUMN co_uuid_1 SET NOT NULL;

ALTER TABLE IF EXISTS th_instituicao_ensino_hist
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_instituicao_ensino_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_instituicao_ensino_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_instituicao_ensino_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_instituicao_ensino_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_instituicao_ensino_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_PESSOA_BANCO e historico
-------------------------------------------------
-- Na TH os tp_operacao e nu_versao estão errados.
-- A dh_alteracao está sendo gravada de forma incorreta (nu_versao = 1).

-------------------------------------------------
-- TB_PROCESSO_SELETIVO e historico
-------------------------------------------------
-- A TH não está gravando todos os registros da TB (mais registros na TB).
-- A TH não está gravando as colunas de segurança,  registro foi desativado mas não gravou a dh_fim_hist.

ALTER TABLE IF EXISTS tb_processo_seletivo
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_processo_seletivo 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_processo_seletivo 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_processo_seletivo 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS tb_processo_seletivo 
ALTER COLUMN co_uuid_1 SET NOT NULL;

ALTER TABLE IF EXISTS th_processo_seletivo_hist
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_processo_seletivo_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_processo_seletivo_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_processo_seletivo_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_processo_seletivo_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_processo_seletivo_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;

-------------------------------------------------
-- TB_RECURSO_CANDIDATURA e historico
-------------------------------------------------
-- Na TB a coluna dh_alteracao está sendo gravada incorretamente, na nu_versao = 1 e tp_operacao = CREATE.
-- Na TH as colunas de dh_alteracao, tp_operacao e nu_versao estão sendo gravadas incorretamente.
-- Na TH a coluna dh_inicio_hist não está funcionando.

ALTER TABLE IF EXISTS tb_recurso_candidatura
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_recurso_candidatura 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS tb_recurso_candidatura 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS tb_recurso_candidatura 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS tb_recurso_candidatura 
ALTER COLUMN co_uuid_1 SET NOT NULL;

ALTER TABLE IF EXISTS th_recurso_candidatura_hist
ALTER COLUMN sg_projeto_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_recurso_candidatura_hist 
ALTER COLUMN sg_acao_modificadora SET NOT NULL;
ALTER TABLE IF EXISTS th_recurso_candidatura_hist 
ALTER COLUMN no_end_point_modificador SET NOT NULL;
ALTER TABLE IF EXISTS th_recurso_candidatura_hist 
ALTER COLUMN dh_criacao SET NOT NULL;
ALTER TABLE IF EXISTS th_recurso_candidatura_hist 
ALTER COLUMN co_uuid_1 SET NOT NULL;
ALTER TABLE IF EXISTS th_recurso_candidatura_hist 
ALTER COLUMN dh_inicio_hist SET NOT NULL;
