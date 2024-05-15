import re
import os

import requests
from dotenv import load_dotenv
from selenium.common import ElementClickInterceptedException, WebDriverException
from selenium.webdriver import Chrome as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from PessoaAtualizar import PessoaAtualizar
from PessoaProcesso import PessoaProcesso
from data_sets.Logger import Logger

load_dotenv()


class PessoasProcessosManager:
    """
    Manager for the relation between Pessoas and Processos\n
    Author: Pedro Henrique Gonçalves Pires\n
    Date: 08/05/2023 -> 09/08/2023\n
    """
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}",
            pool_pre_ping=True
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session: Session = self.Session()

        self.login_url = os.environ['PJE_LOGIN_URL']
        self.search_url = os.environ['PJE_SEARCH_URL']
        self.pje_username = os.environ['PJE_USER']
        self.pje_password = os.environ['PJE_PASSWORD']

        self.success_log_file = os.path.join('logs', 'success.log')
        self.success_logger = Logger('success', self.success_log_file)
        self.errors_logger = Logger('errors', os.path.join('logs', 'errors.log'))
        self.details_logger = Logger('details', os.path.join('logs', 'details.log'))

        self.driver = PessoasProcessosManager.create_driver()

    # ------------------------------------------------------------------------------------------------------------------
    #                                                  PostgreSQL
    # ------------------------------------------------------------------------------------------------------------------
    def reconnect(self):
        """
        Reconecta ao banco de dados
        """
        if self.session.is_active:
            try:
                self.session.close()
            except Exception:
                pass
        self.session = self.Session()

    def select_pessoas_processos(self) -> list[PessoaProcesso]:
        """
        Gets all Pessoas from the PessoaProcesso Table
        :return: List of PessoaProcesso
        """
        self.reconnect()

        pessoas_processos = self.session.query(PessoaProcesso).filter(PessoaProcesso.ativo).all()

        return pessoas_processos

    def select_pessoa_processo(self, uuid_pessoa: str, processo: str) -> PessoaProcesso:
        """
        Gets all Pessoas from the PessoaProcesso Table
        : param uuid_pessoa: uuid of the Pessoa
        : param processo: Processo
        :return: PessoaProcesso
        """
        self.reconnect()

        pessoa_processo = self.session.query(PessoaProcesso).filter(
            PessoaProcesso.ativo,
            PessoaProcesso.uuid_pessoa == uuid_pessoa,
            PessoaProcesso.processo == processo
        ).first()

        return pessoa_processo

    def select_pessoas_atualizar(self, only_in_the_update_line: bool) -> list[PessoaAtualizar]:
        """
        Gets all Pessoas from the Line of to update
        :return: List of Pessoas
        """
        self.reconnect()

        pessoas_atualizar = self.session.query(PessoaAtualizar).all()  # Seleciona todos a pessoas para atualizar
        # Filtra as pessoas que estão na fila de atualização
        if only_in_the_update_line:
            pessoas_atualizar = list(filter(lambda pessoa_atualizar: pessoa_atualizar.is_in_the_atualizacao_line(), pessoas_atualizar))

        return pessoas_atualizar

    def insert_pessoas_processos(self, pessoas_processos: list[PessoaProcesso], audit_fields: dict[str, str], verify_the_existing: bool = False) -> list[str]:
        """
        Inserts Pessoas in the PessoasProcesso Table
        :param pessoas_processos: list of PessoaProcesso to be inserted
        :return: List of Processos inserted
        """
        if not isinstance(pessoas_processos, list):
            pessoas_processos = [pessoas_processos]

        if len(pessoas_processos) == 0:
            return []

        # Verifica se as pessoas_processos já existem no PostgreSQL
        pessoas_processos_to_insert = pessoas_processos
        if verify_the_existing:
            self.details_logger.log('Filtrando os PessoasProcessos novos...', to_print=True)
            # Pega a pessoas_processos identifiers do PostgreSQL
            pessoas_processos_to_insert = [pessoa_processo for pessoa_processo in pessoas_processos
                                           if (self.select_pessoa_processo(pessoa_processo.uuid_pessoa, pessoa_processo.processo) is None)]
            self.details_logger.log('Filtrados os PessoasProcessos novos!')

        self.reconnect()

        # Adiciona os campos de auditoria
        for pessoa_processo in pessoas_processos_to_insert:
            pessoa_processo.set_audit_fields(**audit_fields)

        self.session.add_all(pessoas_processos_to_insert)

        self.session.commit()

        # Pega os números dos processos inseridos
        processos_inserted = [pessoa_processo.processo for pessoa_processo in pessoas_processos_to_insert]

        return processos_inserted

    def reconnect_merge_objects(self, objects: list) -> list:
        self.reconnect()

        # Atualiza o objeto com o banco de dados apos a reconexão
        objects_merged = [self.session.merge(object) for object in objects]

        return objects_merged

    def update_ultima_atualizacao_pessoa_atualizar(self, pessoa_atualizar: list[PessoaAtualizar], audit_fields: dict[str, str]):
        pessoa_atualizar_merged = self.reconnect_merge_objects(pessoa_atualizar)

        for pessoa in pessoa_atualizar_merged:
            pessoa.set_atualizacao_date()
            pessoa.set_audit_fields(**audit_fields)

        self.session.commit()

    # ------------------------------------------------------------------------------------------------------------------
    #                                                  PJe Scrapping
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_driver() -> WebDriver:
        """
        Creates a WebDriver
        """
        # Cria os options para o driver
        options = Options()
        options.add_argument("--start-maximized")  # Maximiza a janela, evitar problemas com a disposição dos elementos
        options.add_argument("--headless")  # Roda o driver em background
        options.add_argument("--no-sandbox")  # Precisa para rodar no linux
        options.add_argument("--remote-debugging-port=9222")  # Precisa para rodar no linux

        # Cria o driver com os options
        driver: WebDriver = WebDriver(options=options)

        return driver

    def quit_driver(self):
        """
        Quits the WebDriver
        """
        self.driver.quit()

    def get_present_element(self, by: str, condition: str, seconds: int = 20):
        """
        Waits for an element to be present in the page
        :param by: Method to find the element
        :param condition: condition to apply the By method
        :param seconds: Seconds to wait
        :return: WebElement
        """
        element = WebDriverWait(self.driver, seconds).until(
            EC.presence_of_element_located((by, condition))
        )

        return element

    def get_clickable_element(self, by: str, condition: str, seconds: int = 20):
        """
        Waits for an element to be present in the page
        :param by: Method to find the element
        :param condition: condition to apply the By method
        :param seconds: Seconds to wait
        :return: WebElement
        """
        element = WebDriverWait(self.driver, seconds).until(
            EC.element_to_be_clickable((by, condition))
        )

        return element

    def login_pje(self):
        """
        Login to PJE
        """
        if self.login_url not in self.driver.current_url:
            self.driver.get(self.login_url)  # Abre a página de login

        while self.login_url in self.driver.current_url:
            # Tenta trocar para o frame de login se ele estiver presente
            try:
                login_frame = self.get_present_element(By.ID, 'ssoFrame')  # Encontra o frame de login
                self.driver.switch_to.frame(login_frame)  # Entra no frame de login
            except Exception as e:
                pass

            # Preenche o usuário e a senha e clica em login
            self.get_present_element(By.ID, 'username').send_keys(self.pje_username)
            self.get_present_element(By.ID, 'password').send_keys(self.pje_password)
            try:
                self.get_clickable_element(By.XPATH, '//*[@value="Entrar"]').click()
            except WebDriverException:  # Se deu erro na página após clicar
                pass  # Continua o loop
            self.driver.refresh()  # Atualiza a página

    def wait_pje_search_load(self):
        # Espera a pesquisa carregar
        carregou_resultados: bool = False
        while not carregou_resultados:
            # Verifica se o style do span que aparece o carregamento mudou, ele fica vazio quando carrega
            if self.driver.find_element(By.XPATH, '//*[@id="_viewRoot:status.start"]').get_attribute('style') != '':
                carregou_resultados = True

    def search_processo_by_pessoa(self, pessoa: PessoaAtualizar) -> list[PessoaProcesso]:
        """
        Search for a Processo by Pessoa
        :param pessoa: Pessoa to search the Processos and Add them
        :return: status code 1/0
        """
        while self.search_url not in self.driver.current_url:
            self.driver.get(self.search_url)
            if self.login_url in self.driver.current_url:
                self.login_pje()

        self.wait_pje_search_load()  # Garante que a página carregou internamente

        # Alguns loopings de tentativa de clicar são necessários para não exceder o limite de recursão da função

        # Fica em loop ate conseguir clicar no radio button, pois as vezes ele não conseguia clicar e dava erro
        clicked_radio: bool = False
        while not clicked_radio:
            # Verifica se a pessoa é PJ ou PF e seleciona o tipo de pesquisa
            try:
                is_pj = pessoa.is_pj()
                if is_pj:
                    self.driver.find_element(By.XPATH, '//*[@id="cnpj"]').click()
                elif is_pj is not None:
                    self.driver.find_element(By.XPATH, '//*[@id="cpf"]').click()
                else:
                    raise ValueError('Tipo de pessoa inválido!')

                clicked_radio = True
            except ElementClickInterceptedException:
                clicked_radio = False

        # Pesquisa pelo documento
        self.driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]').clear()  # Limpa o campo antes de pesquisar
        self.driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]').send_keys(pessoa.get_documento())  # Digita o documento

        # Fica em loop até consegui apertar o botão pesquisar, pois às vezes ele não conseguia clicar e dava erro
        clicked_search: bool = False
        while not clicked_search:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="fPP:searchProcessos"]').click()  # Clica no botão pesquisar
                clicked_search = True
            except ElementClickInterceptedException:
                clicked_search = False

        self.wait_pje_search_load()  # Espera a pesquisa carregar

        # Verifica se o documento buscado foi dado como valido
        error_message = self.driver.find_element(By.XPATH, '//*[@id="fPP:j_id468"]')
        if error_message.text != '':
            return []

        # Ensures it is on the 1st page of the result,
        # because if the last search had more pages it will not be on the first page
        self.driver.find_element(By.XPATH, '//*[@id="fPP:processosTable:scTabela_table"]/tbody/tr/td[1]').click()  # TODO: Talvez olhar se prende em looping tbm
        self.wait_pje_search_load()  # Espera a pesquisa carregar

        # Busca por cada página do resultado
        pessoa_processos = []
        while True:
            # Garante que a pesquisa vai estar carregada
            self.wait_pje_search_load()

            # Pega os números dos processos da página atual
            tabela = self.driver.find_element(By.XPATH, '//*[@id="fPP:processosTable"]')
            tags_as_processos = tabela.find_elements(By.TAG_NAME, 'a')
            # Itera por cada processo listado
            for tag_a_processo in tags_as_processos:
                processo = re.sub('[^0-9]', '', tag_a_processo.text)
                pessoa_processos.append(PessoaProcesso(uuid_pessoa=pessoa.uuid_pessoa,
                                                       processo=processo))

            # Verifica se tem próxima página
            menu_paginacao = self.driver.find_element(By.XPATH, '//*[@id="fPP:processosTable:scTabela_table"]/tbody/tr')
            botoes_paginacao = menu_paginacao.find_elements(By.TAG_NAME, 'td')
            botao_proximo = botoes_paginacao[-2]  # O botão de próxima página é o penúltimo

            # Se o botão de próxima página está desabilitado, não tem mais páginas
            if 'dsbld' in botao_proximo.get_attribute('class'):  # TODO: possívelmente usar a ausência de 'onclick' para não correr o risco de cair em erro de CSS
                break  # Sai do loop

            botao_proximo.click()  # Vai para próxima página

        return pessoa_processos

    def get_processos_from_pje_until_break(self, pessoas: list[PessoaAtualizar]) -> (list[PessoaProcesso], list[PessoaAtualizar]):
        """
        Get Processos from PJE until one search fails
        :param pessoas: Pessoas to search the Processos and Add them
        :return: Pessoas Processos that were searched, Pessoas that were not searched
        """
        pessoas_processos_pje: list[PessoaProcesso] = []  # Lista de pessoas processos que foram encontrados

        pessoas_already_searched: list = []  # Lista de pessoas que já foram tentados

        pessoa_that_failed = None  # Pessoa que deu erro

        for pessoa in pessoas:
            try:
                pessoas_processos_pje.extend(self.search_processo_by_pessoa(pessoa))  # Tenta pesquisar

                pessoas_already_searched.append(pessoa)  # Adiciona a lista de assistidos já tentados
                self.success_logger.log(f"Processos encontrados para: {pessoa.uuid_pessoa}")
            except Exception as e:
                # Se não conseguir pesquisar, dá erro e para o loop
                pessoa_that_failed = pessoa
                message: str = f"Error: {{{e}}} searching processos for: {pessoa.uuid_pessoa}"
                self.errors_logger.log(message, to_warn=True)
                break

        # Separa as pessoas que já foram tentados dos que não foram
        pessoas_not_searched: list = [pessoa for pessoa in pessoas if (pessoa not in pessoas_already_searched)]
        # Manda a pessoa que deu erro para o final da lista
        if pessoa_that_failed is not None:
            pessoas_not_searched.remove(pessoa_that_failed)  # Remove a pessoa que deu erro
            pessoas_not_searched.append(pessoa_that_failed)  # Adiciona o pessoa que deu erro no final da lista

        return pessoas_processos_pje, pessoas_not_searched

    # ------------------------------------------------------------------------------------------------------------------
    #                                                  ProcAPI
    # ------------------------------------------------------------------------------------------------------------------
    def send_processos_to_procapi(self, processos: list[str]) -> None:
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
        for processo in processos:
            # Envia o processo
            response = requests.get(f"{os.environ['URL_PROCAPI']}processos/{processo}/", headers=headers)

            # Verifica se deu erro
            if response.status_code != 200:
                self.errors_logger.log(f"Error sending Processo {processo} to ProcAPI: {response.text}", to_warn=True)

    # ------------------------------------------------------------------------------------------------------------------
    #                                                  PJe - > PostgreSQL
    # ------------------------------------------------------------------------------------------------------------------
    def monitor_pessoas_to_update(self):
        """
        Monitor the Pessoas to update
        :return: status code 1/0
        """
        audit_fields_pessoa_processo = {
            'projeto_modificador': 'ASSPRO',
            'acao_modificadora': 'INSNOVPESPRO',
            'end_point_modificador': 'rotina/monitor_pessoas_to_update',
            'uuid_usuario_modificador': 'ASSISTIDO-PROCESSO-PYTHON',
        }
        audit_fields_pessoa_atualizar = {
            'projeto_modificador': 'ASSPRO',
            'acao_modificadora': 'MARPESATU',
            'end_point_modificador': 'rotina/monitor_pessoas_to_update',
            'uuid_usuario_modificador': 'ASSISTIDO-PROCESSO-PYTHON',
        }

        # Configura o PJe
        self.details_logger.log('Fazendo Login no PJe...', to_print=True)
        self.login_pje()
        self.details_logger.log('Login Feito!')

        # Monitora a fila de Pessoas para Atualizar
        self.details_logger.log('Monitorando a fila de Pessoas para Atualizar...', to_print=True)
        while True:
            try:
                # Pega as pessoas para atualizar
                pessoas_to_update = self.select_pessoas_atualizar(only_in_the_update_line=True)

                # Se tiver pessoas para atualizar
                if len(pessoas_to_update) > 0:
                    # Pega os processos das pessoas para atualizar
                    self.details_logger.log(f'Atualizando as Pessoas...', to_print=True)
                    pessoas_processos_searched, pessoas_not_updated = self.get_processos_from_pje_until_break(pessoas_to_update)

                    # Se tinha processos
                    processos_inserted = []
                    if len(pessoas_processos_searched) > 0:
                        # Insere os processos no banco de dados
                        processos_inserted = self.insert_pessoas_processos(pessoas_processos_searched, audit_fields_pessoa_processo, verify_the_existing=True)

                    self.details_logger.log(f'Pessoas Processos atualizados!')

                    # Seta a data de atualização das pessoas atualizados
                    self.details_logger.log(f'Atualizando a data de atualização das Pessoas...', to_print=True)
                    pessoas_updated = [pessoa for pessoa in pessoas_to_update if pessoa not in pessoas_not_updated]
                    self.update_ultima_atualizacao_pessoa_atualizar(pessoas_updated, audit_fields_pessoa_atualizar)
                    self.details_logger.log(f'Data de atualização das Pessoas atualizada!')

                    # Envia os processos para o ProcAPI
                    self.details_logger.log(f'Enviando os Processos para o ProcAPI...', to_print=True)
                    self.send_processos_to_procapi(processos_inserted)
                    self.details_logger.log(f'Processos enviados para o ProcAPI!')

                    self.details_logger.log('Monitorando a fila de Pessoas para Atualizar...', to_print=True)
            except Exception as e:
                self.errors_logger.log(f'Erro no monitoramento: {{{e}}}', to_warn=True)


# ----------------------------------------------------------------------------------------------------------------------
#                                                       Main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    Test and Example of use
    """
    pessoas_processos_manager = PessoasProcessosManager()  # Cria o PessoasProcessosManager

    # pessoas_processos_manager.insert_new_pessoas_processos()  # Insere os novos PessoaProcesso

    pessoas_processos_manager.monitor_pessoas_to_update()  # Monitora a fila de pessoas para atualizar
