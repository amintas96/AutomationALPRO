from selenium import webdriver
from selenium.webdriver.common.by import By
from Mapped import Components as Cp
from datetime import datetime

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
dv = webdriver.Chrome()



def do_registration(username, password, data, activity):
    try:
        dv.get(Cp.SITE)
        dv.maximize_window()
        dv.find_element(By.XPATH, Cp.xpath_user).send_keys(username)
        dv.find_element(By.XPATH, Cp.xpath_password).send_keys(password)
        dv.find_element(By.XPATH, Cp.xpath_enter_inicial).click()


        if data:
            data_objeto = datetime.strptime(data, "%d/%m/%Y")
            data_formatada = data_objeto.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data_formatada)
        else:
            data_hoje = datetime.today()
            data_formatada = data_hoje.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data_formatada)


        #Parte inicial do registro do ponto
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial).send_keys(activity)
        dv.find_element(By.XPATH, Cp.xpath_horario_inicial).send_keys("8:00")
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial).send_keys("4:00")

        #Parte Descanso do registro

        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace("tr[1]", "tr[2]")).send_keys(Cp.INTERVAL)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial.replace("tr[1]", "tr[2]")).send_keys("1:00")

        #Parte final do registro do ponto

        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace("tr[1]", "tr[3]")).send_keys(activity)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial.replace("tr[1]", "tr[3]")).send_keys("4:00")

        dv.find_element(By.XPATH, Cp.xpath_registra_atividade).click()
    except Exception as e:
        print(str(e))

do_registration(username="amintas.neto@mirante.net.br", password="Miojo@121996",
              activity="Petrobras/Vigência 1/Serviços/Projetos/Apurar Receitas (SATE)/Sprint 08/Sprint 08 - Reunião-Ata", data='17/05/2024')





