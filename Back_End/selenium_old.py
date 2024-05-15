#python -m venv env, cd env, \Scripts\activate, 
# Set-ExecutionPolicy Unrestricted -Force (caso de erro), Set-ExecutionPolicy  -Scope CurrentUser  -ExecutionPolicy RemoteSigned
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

nav = webdriver.Chrome() # Utiliza o navegador Chrome

nav.get("https://tst.gerais.mg.def.br/sistemas/scsdp/") # Entra nesse site
time.sleep(2)

nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[1]/div/div[2]').click() # Login
time.sleep(0.5)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/label[1]/div/div[1]/div[2]/input').send_keys("08515583640")
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/label[2]/div/div[1]/div[2]/input').send_keys("")
time.sleep(1)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/div/div[1]/div/button').click() # Entra no DPMG
nav.find_element(By.XPATH, '/html/body/div[1]/div/header/div[1]/button[1]').click() # Entra na aba lateral

input()

# COPY ELEMENT --> <input class="q-field__native q-placeholder" tabindex="0" aria-label="Nome*" name="pessoa.nome" id="f_0aed27e2-a69a-48d8-b092-88a54942410b" type="text">