from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from Mapped import Components as Cp
from datetime import datetime, timedelta, time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as tm


def do_login(dv, username, password):
    try:
        dv.get(Cp.SITE)
        dv.implicitly_wait(2)
        dv.maximize_window()
        dv.find_element(By.XPATH, Cp.xpath_user).send_keys(username)
        dv.find_element(By.XPATH, Cp.xpath_password).send_keys(password)
        dv.find_element(By.XPATH, Cp.xpath_enter_inicial).click()
        dv.implicitly_wait(0.5)
        while valida_botao_inicial(dv):
            pass
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
    
def ler_parametros(arquivo):
    parametros = {}
    with open(arquivo, 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split(':')
            try:
                value = str(value.strip())
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            parametros[key] = value
    return parametros

def last_registration(dv,json):

    try:
        username = json['username']
        password = json['password']
        tentativas = 0
        for i in range(3):
            if do_login(dv, username, password):
                break
            tentativas += 1
        if tentativas >= 3:
            raise Exception("Falha durante o processo de login")
        new_date = datetime.today()

        while not valid_registration_by_date(dv, new_date):
            tm.sleep(1)        
            new_date = new_date - timedelta(days=1)

        return new_date

    except Exception as e:
        print(str(e))



def registre_points(json):
    # options.add_argument("--headless")
    try:
        dv = webdriver.Edge()
        new_date = datetime.today()
        last_registre = last_registration(dv, json)

        while last_registre < new_date:
            last_registre = last_registre + timedelta(days=1) 
            if last_registre.weekday() < 5:
                json['data'] = last_registre.strftime("%Y-%m-%d")
                do_registration(dv, json)
    except Exception as e:
        print(str(e))

def valid_registration_by_date(dv, date):
    try:    
        date_formatada = date.strftime("%Y-%m-%d")
        dv.get(Cp.SITE_DATA + date_formatada)
        horario = dv.find_element(By.XPATH, Cp.xpath_total_horas).get_attribute('value')
        return horario if pode_ser_hora(horario) and datetime.strptime(horario, '%H:%M').time() >= time(5, 0) else False
            
    except Exception as e:
        print(str(e))
        return False

def gerar_horario_com_diferenca():
    # Gerar horário aleatório entre 3:45 e 4:00
    inicio_minutos = 3 * 60 + 45  # 3:45 em minutos
    fim_minutos = 4 * 60 + 0      # 4:00 em minutos
    minutos_totais = random.randint(inicio_minutos, fim_minutos)
    
    # Converter para horas e minutos
    hora = minutos_totais // 60
    minutos = minutos_totais % 60
    horario_gerado = f"{hora}:{minutos:02d}"
    
    # Calcular diferença até 8:00 (em minutos)
    minutos_8h = 8 * 60  # 8:00 em minutos
    diferenca_minutos = minutos_8h - minutos_totais
    
    # Converter diferença para H:MM
    diferenca_hora = diferenca_minutos // 60
    diferenca_minuto = diferenca_minutos % 60
    horario_diferenca = f"{diferenca_hora}:{diferenca_minuto:02d}"
    
    return horario_gerado, horario_diferenca

def pode_ser_hora(string, formato='%H:%M'):
    try:
        datetime.strptime(string, formato)
        return True
    except ValueError as e:
        print(str(e))
        return False
    
def valida_botao_inicial(dv):
    try:
        elemento = WebDriverWait(dv, 3).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/form/fieldset/table/tbody/tr/td[1]/div[1]/table/tbody/tr/td[2]/button'))
        )
        elemento.click()
        tm.sleep(2)  
        print("Botão inicial encontrado e clicado.")
        return True  
    except Exception as e:
        return False  
    
    
def do_registration(dv, json):
    try:
        data = json['data']
        activity = json['activity']
        hora = generate_hour_by_validation(dv)

        if data:
            # data_objeto = datetime.strptime(data, "%d/%m/%Y")
            # data_formatada = data.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data)
        else:
            data_hoje = datetime.today()
            data_formatada = data_hoje.strftime("%Y-%m-%d")
            dv.get(Cp.SITE_DATA + data_formatada)

        if dv.find_element(By.XPATH, Cp.xpath_horario_inicial).get_attribute('value'):
            clear_fields(dv)
        trabalhado, dif = gerar_horario_com_diferenca()
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial).send_keys(activity)
        dv.find_element(By.XPATH, Cp.xpath_horario_inicial).send_keys(hora)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial).send_keys(trabalhado)
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace("tr[1]", "tr[2]")).send_keys(Cp.INTERVAL)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial.replace("tr[1]", "tr[2]")).send_keys("1:00")
        dv.find_element(By.XPATH, Cp.xpath_atividade_inicial.replace("tr[1]", "tr[3]")).send_keys(activity)
        dv.find_element(By.XPATH, Cp.xpath_fimHora_inicial.replace("tr[1]", "tr[3]")).send_keys(dif)

        dv.find_element(By.XPATH, Cp.xpath_registra_atividade).click()

        return {'Sucesso': True, 'Mensagem': "Registro realizado com sucesso"}
    except Exception as e:
        return {'Sucesso': False, 'Mensagem': f" Falha no registro: {e}"}

