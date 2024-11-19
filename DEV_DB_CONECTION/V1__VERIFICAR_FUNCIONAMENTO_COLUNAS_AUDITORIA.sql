----------------------------------------------------------------------------------------------------
-- VERIFICA SE AS COLUNAS DE AUDITORIA EXISTEM E ESTÃO FUNCIONANDO CORRETAMENTE, NO SCHEMA INFORMADO
----------------------------------------------------------------------------------------------------

-- adicionar a condicao de, se a dh_fim_hist existir e o tp_operacao for CREATE OU UPDATE as colunas da th não estão funcionando corretamente.
-- Adicionar as outras condições de obrigatoriedade para TODAS as colunas menos dh_alteracao e _hist, mostrando uma mensagem para cada coluna.

-- O erro deve mostrar exatamente cada problema.

DO $$
DECLARE
    nome_schema                   TEXT := 'cesv'; -- INFORME O SCHEMA QUE DESEJA ITERAR
    reg1_tabela                   RECORD;
    th_correspondente             RECORD;
    -- Verifica colunas de auditoria da tb
    tb_coluna_projeto_existe      RECORD;
    tb_coluna_acao_existe         RECORD;
    tb_coluna_endpoint_existe     RECORD;
    tb_coluna_preenchida          RECORD;
    tb_coluna_acao_preenchida     RECORD;
    tb_coluna_endpoint_preenchida RECORD;
    -- Verifica colunas de auditoria da th
    th_coluna_projeto_existe      RECORD;
    th_coluna_acao_existe         RECORD;
    th_coluna_endpoint_existe     RECORD;
    th_coluna_preenchida          RECORD;
    th_coluna_acao_preenchida     RECORD;
    th_coluna_endpoint_preenchida RECORD;

    tb_coluna                     RECORD;

    valor_co_seq_tb               INTEGER;
    valor_co_seq_th               INTEGER;
    co_seq_tb                     TEXT;
    co_seq_th                     TEXT;
    tb_tem_registros              BOOLEAN;
    th_tem_registros              BOOLEAN;
BEGIN
    -- SELECIONA A TABELA PRINCIPAL
    FOR reg1_tabela IN 
        SELECT DISTINCT(table_name)
        FROM information_schema.tables
        WHERE table_name LIKE 'tb_%'
          AND table_schema = nome_schema
        ORDER BY table_name
    LOOP
        RAISE NOTICE 'Iterando pela Tabela: % e tabela histórico', reg1_tabela.table_name;

        -- Verificar se a coluna de auditoria: sg_projeto_modificador, existe e tem registro na tb
        SELECT * 
        INTO tb_coluna_projeto_existe
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name = 'sg_projeto_modificador'
        LIMIT 1;

        IF tb_coluna_projeto_existe IS NULL THEN
            RAISE NOTICE "ALTER TABLE %.% ADD COLUMN sg_projeto_modificador varchar(100) NOT NULL;
                          COMMENT ON COLUMN %.%.sg_projeto_modificador IS 'Sigla do projeto que iniciou o processo modificador do dado.';", 
                          nome_schema, reg1_tabela.table_name, nome_schema, reg1_tabela.table_name;
        ELSE
            -- Verificar se a coluna de auditoria: sg_projeto_modificador, esta preenchida
            EXECUTE format('
                SELECT sg_projeto_modificador
                FROM %I.%I
                WHERE sg_projeto_modificador IS NOT NULL
                LIMIT 1', 
                nome_schema, reg1_tabela.table_name)
            INTO tb_coluna_projeto_preenchida;

            IF tb_coluna_projeto_preenchida IS NULL THEN
                RAISE NOTICE '...Coluna: SG_PROJETO_MODIFICADOR, NAO PREENCHIDA na tabela: %', reg1_tabela.table_name;
            END IF;
        END IF;

        -- Verificar se a coluna de auditoria: sg_acao_modificadora, existe e tem registro na tb
        SELECT * 
        INTO tb_coluna_acao_existe
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name = 'sg_acao_modificadora'
        LIMIT 1;

        IF tb_coluna_acao_existe IS NULL THEN
            RAISE NOTICE "ALTER TABLE %.% ADD COLUMN sg_acao_modificadora varchar(100) NOT NULL;
                          COMMENT ON COLUMN %.%.sg_acao_modificadora IS 'Sigla da acao do processo modificador do dado.';",
                          nome_schema, reg1_tabela.table_name, nome_schema, reg1_tabela.table_name;
        ELSE
            -- Verificar se a coluna de auditoria: sg_acao_modificadora, esta preenchida
            EXECUTE format('
                SELECT sg_acao_modificadora
                FROM %I.%I
                WHERE sg_acao_modificadora IS NOT NULL
                LIMIT 1',
                nome_schema, reg1_tabela.table_name)
            INTO tb_coluna_acao_preenchida;

            IF tb_coluna_acao_preenchida IS NULL THEN
                RAISE NOTICE '...Coluna: SG_ACAO_MODIFICADORA, NAO PREENCHIDA na tabela: %', reg1_tabela.table_name;
            END IF;
        END IF;

        SELECT * 
        INTO tb_coluna_endpoint_existe
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name = 'no_end_point_modificador'
        LIMIT 1;
       
        IF tb_coluna_endpoint_existe IS NULL THEN
            RAISE NOTICE "ALTER TABLE %.% ADD COLUMN no_end_point_modificador varchar(255) NOT NULL;
                          COMMENT ON COLUMN %.%.no_end_point_modificador IS 'Nome do end point que iniciou o processo modificador do dado.';",
                          nome_schema, reg1_tabela.table_name, nome_schema, reg1_tabela.table_name;
        ELSE
            -- Verificar se a coluna de auditoria: no_end_point_modificador,  esta preenchida
            EXECUTE format('
                SELECT no_end_point_modificador
                FROM %I.%I
                WHERE no_end_point_modificador IS NOT NULL
                LIMIT 1',
                nome_schema, reg1_tabela.table_name) 
            INTO tb_coluna_endpoint_preenchida;

            IF tb_coluna_endpoint_preenchida IS NULL THEN
                RAISE NOTICE '...Coluna: NO_END_POINT_MODIFICADOR, NAO PREENCHIDA na tabela: %', reg1_tabela.table_name;
            END IF;
        END IF;

        -- Verificar condições com base no valor da nu_versao
        EXECUTE format('SELECT nu_versao, tp_operacao, dh_criacao, dh_alteracao, st_ativo FROM %I.%I LIMIT 1', nome_schema, reg1_tabela.table_name)
        INTO tb_coluna;

        IF tb_coluna.nu_versao = 1 THEN
            -- Verifica para a versão inicial
            IF tb_coluna.tp_operacao != 'CREATE' OR tb_coluna.dh_criacao IS NULL OR tb_coluna.dh_alteracao IS NOT NULL THEN
                RAISE NOTICE '......TABELA: %, NÃO ESTÁ GRAVANDO A VERSÃO INICIAL CORRETAMENTE.', reg1_tabela.table_name;
            END IF;
        ELSE
            -- Verifica para as versões posteriores
            IF tb_coluna.tp_operacao NOT IN ('UPDATE', 'DELETE', 'VIEW') OR tb_coluna.dh_criacao IS NULL OR tb_coluna.dh_alteracao IS NULL THEN
                RAISE NOTICE '......TABELA: %, NÃO ESTÁ GRAVANDO AS VERSÕES POSTERIORES CORRETAMENTE.', reg1_tabela.table_name;
            END IF;
        END IF;

        -- Verificar a operação DELETE
        IF tb_coluna.tp_operacao = 'DELETE' AND tb_coluna.st_ativo THEN
            RAISE NOTICE '......TABELA: %, NÃO ESTÁ INATIVANDO OS REGISTROS CORRETAMENTE', reg1_tabela.table_name;
        END IF;

        -- Identifica a coluna LIKE 'co_seq%' da tabela principal
        SELECT column_name
        INTO co_seq_tb
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name LIKE 'co_seq%'
        LIMIT 1;

        IF co_seq_tb IS NULL THEN
            RAISE NOTICE '......Coluna co_seq: % NÃO ENCONTRADA na tabela principal: %', co_seq_tb, reg1_tabela.table_name;
            CONTINUE;
        END IF;

        -- Verifica se há registros na tabela principal
        EXECUTE format('SELECT EXISTS (SELECT 1 FROM %I.%I)', nome_schema, reg1_tabela.table_name)
        INTO tb_tem_registros;

        IF NOT tb_tem_registros THEN
            RAISE NOTICE '......Tabela principal % está vazia.', reg1_tabela.table_name;
            CONTINUE;
        END IF;

        -- Seleciona a tabela histórica correspondente
        SELECT DISTINCT(table_name)
        INTO th_correspondente
        FROM information_schema.tables
        WHERE table_name = 'th_' || substring(reg1_tabela.table_name from 4) || '_hist'
          AND table_schema = nome_schema;

        IF th_correspondente.table_name IS NULL THEN
            RAISE NOTICE '......Tabela histórica correspondente NÃO ENCONTRADA para %', reg1_tabela.table_name;
            CONTINUE;
        END IF;

        -- Verificar se as colunas de auditoria existem na tabela histórica
        -- Verificar se a coluna de auditoria: sg_projeto_modificador, existe e tem registro na th
        SELECT * 
        INTO th_coluna_projeto_existe
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name = 'sg_projeto_modificador'
        LIMIT 1;

        IF th_coluna_projeto_existe IS NULL THEN
            RAISE NOTICE "ALTER TABLE %.% ADD COLUMN sg_projeto_modificador varchar(100) NOT NULL;
                          COMMENT ON COLUMN %.%.sg_projeto_modificador IS 'Sigla do projeto que iniciou o processo modificador do dado.';",
                          nome_schema, reg1_tabela.table_name, nome_schema, reg1_tabela.table_name;
        ELSE
            -- Verificar se a coluna de auditoria: sg_projeto_modificador, esta preenchida
            EXECUTE format('
                SELECT sg_projeto_modificador
                FROM %I.%I
                WHERE sg_projeto_modificador IS NOT NULL
                LIMIT 1', 
                nome_schema, reg1_tabela.table_name)
            INTO th_coluna_projeto_preenchida;

            IF th_coluna_projeto_preenchida IS NULL THEN
                RAISE NOTICE '...Coluna: SG_PROJETO_MODIFICADOR, NAO PREENCHIDA na tabela: %', reg1_tabela.table_name;
            END IF;
        END IF;

        -- Verificar se a coluna de auditoria: sg_acao_modificadora, existe e tem registro na tb
        SELECT * 
        INTO th_coluna_acao_existe
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name = 'sg_acao_modificadora'
        LIMIT 1;

        IF th_coluna_acao_existe IS NULL THEN
            RAISE NOTICE "ALTER TABLE %.% ADD COLUMN sg_acao_modificadora varchar(100) NOT NULL;
                          COMMENT ON COLUMN %.%.sg_acao_modificadora IS 'Sigla da acao do processo modificador do dado.';",
                          nome_schema, reg1_tabela.table_name, nome_schema, reg1_tabela.table_name;
        ELSE
            -- Verificar se a coluna de auditoria: sg_acao_modificadora, esta preenchida
            EXECUTE format('
                SELECT sg_acao_modificadora
                FROM %I.%I
                WHERE sg_acao_modificadora IS NOT NULL
                LIMIT 1',
                nome_schema, reg1_tabela.table_name)
            INTO th_coluna_acao_preenchida;

            IF th_coluna_acao_preenchida IS NULL THEN
                RAISE NOTICE '...Coluna: SG_ACAO_MODIFICADORA, NAO PREENCHIDA na tabela: %', reg1_tabela.table_name;
            END IF;
        END IF;

        SELECT * 
        INTO th_coluna_endpoint_existe
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = reg1_tabela.table_name
          AND column_name = 'no_end_point_modificador'
        LIMIT 1;
       
        IF th_coluna_endpoint_existe IS NULL THEN
            RAISE NOTICE "ALTER TABLE %.% ADD COLUMN no_end_point_modificador varchar(255) NOT NULL;
                          COMMENT ON COLUMN %.%.no_end_point_modificador IS 'Nome do end point que iniciou o processo modificador do dado.';",
                          nome_schema, reg1_tabela.table_name, nome_schema, reg1_tabela.table_name;
        ELSE
            -- Verificar se a coluna de auditoria: no_end_point_modificador,  esta preenchida
            EXECUTE format('
                SELECT no_end_point_modificador
                FROM %I.%I
                WHERE no_end_point_modificador IS NOT NULL
                LIMIT 1',
                nome_schema, reg1_tabela.table_name) 
            INTO th_coluna_endpoint_preenchida;

            IF th_coluna_endpoint_preenchida IS NULL THEN
                RAISE NOTICE '...Coluna: NO_END_POINT_MODIFICADOR, NAO PREENCHIDA na tabela: %', reg1_tabela.table_name;
            END IF;
        END IF;

        -- Identifica a coluna LIKE 'co_seq%' da tabela histórica
        SELECT column_name
        INTO co_seq_th
        FROM information_schema.columns
        WHERE table_schema = nome_schema
          AND table_name = th_correspondente.table_name
          AND column_name LIKE 'co_seq%'
        LIMIT 1;

        IF co_seq_th IS NULL THEN
            RAISE NOTICE '......Coluna co_seq: % NÃO ENCONTRADA na tabela histórica: %', co_seq_th, th_correspondente.table_name;
            CONTINUE;
        END IF;

        -- Verificar se há registros na tabela histórica
        EXECUTE format('SELECT EXISTS (SELECT 1 FROM %I.%I)', nome_schema, th_correspondente.table_name)
        INTO th_tem_registros;

        IF NOT th_tem_registros THEN
            RAISE NOTICE '......Tabela histórica % está vazia.', th_correspondente.table_name;
            CONTINUE;
        END IF;

        -- Obtém o valor máximo de co_seq na tabela principal
        EXECUTE format('SELECT MAX(%I) FROM %I.%I', co_seq_tb, nome_schema, reg1_tabela.table_name)
        INTO valor_co_seq_tb;

        -- Obtém o valor máximo de co_seq na tabela histórica
        EXECUTE format('SELECT MAX(%I) FROM %I.%I', co_seq_th, nome_schema, th_correspondente.table_name)
        INTO valor_co_seq_th;

        -- Compara os valores máximos de co_seq
        IF valor_co_seq_tb IS NULL OR valor_co_seq_th IS NULL THEN
            RAISE NOTICE '......Não há registros para comparação entre % e %', reg1_tabela.table_name, th_correspondente.table_name;
        ELSEIF valor_co_seq_tb > valor_co_seq_th THEN
            RAISE NOTICE '......Tabela principal % NÃO está gravando os registros na tabela histórica % corretamente', reg1_tabela.table_name, th_correspondente.table_name;
        ELSE
            RAISE NOTICE '......Tabela principal % está gravando os registros na tabela histórica % corretamente', reg1_tabela.table_name, th_correspondente.table_name;
        END IF;

    END LOOP;
END $$;
