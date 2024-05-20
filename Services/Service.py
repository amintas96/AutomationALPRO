from click.parser import Option
from selenium import webdriver
from selenium.webdriver.common.by import By
from Mapped import Components as Cp
from datetime import datetime


def do_login(dv, username, password):
    try:
        dv.get(Cp.SITE)
        dv.maximize_window()
        dv.find_element(By.XPATH, Cp.xpath_user).send_keys(username)
        dv.find_element(By.XPATH, Cp.xpath_password).send_keys(password)
        dv.find_element(By.XPATH, Cp.xpath_enter_inicial).click()
        return True
    except Exception as e:
        return False


def clear_fields(dv):
    try:
        dv.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/form[2]/fieldset/table/tbody/tr[4]/td[5]/input').clear()
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial).clear()
        dv.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/form[2]/fieldset/table/tbody/tr[3]/td[5]/input').clear()
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace('tr[1]', 'tr[2]')).clear()
        dv.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/form[2]/fieldset/table/tbody/tr[2]/td[5]/input').clear()
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace('tr[1]', 'tr[3]')).clear()
        dv.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/form[2]/fieldset/table/tbody/tr[1]/td[5]/input').clear()
    except Exception as e:
        raise Exception(f"falha durante a limpeza dos campos:  {e}!")


def do_registration(json):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    dv = webdriver.Chrome(options=options)
    try:

        username = json['username']
        password = json['password']
        data = json['data']
        activity = json['activity']

        tentativas = 0
        for i in range(3):
            if do_login(dv, username, password):
                break
            tentativas += 1
        if tentativas >= 3:
            raise Exception("Falha durante o processo de login")

        if data:
            data_objeto = datetime.strptime(data, "%d/%m/%Y")
            data_formatada = data_objeto.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data_formatada)
        else:
            data_hoje = datetime.today()
            data_formatada = data_hoje.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data_formatada)

        if dv.find_element(By.XPATH, Cp.xpath_horario_inicial).get_attribute('value'):
            clear_fields(dv)

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
        return {'Sucesso': True, 'Mensagem': "Registro realizado com sucesso"}
    except Exception as e:
        return {'Sucesso': False, 'Mensagem': f" Falha no registro: {e}"}
