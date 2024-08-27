from selenium import webdriver
from selenium.webdriver.common.by import By
from Mapped import Components as Cp
from datetime import datetime, timedelta
import random


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


def generate_hour():
    hour = random.randrange(0, 12)
    if hour >= 10:
        return "08:" + str(hour)
    else:
        return "08:0" + str(hour)


def valid_last_7_days(dv):
    try:
        list_hours = []
        for i in range(1, 8):
            last_date = datetime.today() - timedelta(days=i)
            data_formatada = last_date.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data_formatada)
            list_hours.append(dv.find_element(By.XPATH, Cp.xpath_horario_inicial).get_attribute('value'))

        return list_hours
    except Exception as e:
        print("falha + " + str(e))


def generate_hour_by_validation(dv):
    hora = generate_hour()
    while hora in valid_last_7_days(dv):
        hora = generate_hour()
    else:
        return str(hora)


def do_registration(json):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
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
        hora = generate_hour_by_validation(dv)
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

        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial).send_keys(activity)
        dv.find_element(By.XPATH, Cp.xpath_horario_inicial).send_keys(hora)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial).send_keys("4:00")

        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace("tr[1]", "tr[2]")).send_keys(Cp.INTERVAL)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial.replace("tr[1]", "tr[2]")).send_keys("1:00")

        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace("tr[1]", "tr[3]")).send_keys(activity)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial.replace("tr[1]", "tr[3]")).send_keys("4:00")

        dv.find_element(By.XPATH, Cp.xpath_registra_atividade).click()
        return {'Sucesso': True, 'Mensagem': "Registro realizado com sucesso"}
    except Exception as e:
        return {'Sucesso': False, 'Mensagem': f" Falha no registro: {e}"}
