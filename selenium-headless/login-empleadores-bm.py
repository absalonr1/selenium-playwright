from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time
import os

# Ruta al ChromeDriver (ajusta según tu sistema)

# Configuración del WebDriver
options = Options()
options.add_argument("--start-maximized")  # Inicia el navegador maximizado
options.add_argument("--headless")  # Ejecutar en modo headless
options.add_argument("window-size=1024,780")
#options.add_argument("--disable-gpu")  # Acelerar en sistemas no gráficos
#options.add_argument("--no-sandbox")  # Para sistemas tipo Linux
#options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memoria compartida

driver = webdriver.Firefox( options=options)

try:
    # Navega a una URL
    url = "https://login-empleadores.isaprebanmedica.cl/login/"
    driver.get(url)

    # Espera para asegurarse de que la página cargue
    time.sleep(2)

   
   
    rut_emp_field = driver.find_element(By.ID, "rutempresa")
    rut_emp_field.send_keys(os.getenv('LOGIN_EMP_BM_RUTEMP'))

    rut_usr_field = driver.find_element(By.ID, "rutusuario")
    rut_usr_field.send_keys(os.getenv('LOGIN_EMP_BM_RUTUSR'))

    rut_usr_field = driver.find_element(By.ID, "current-password")
    rut_usr_field.send_keys(os.getenv('LOGIN_EMP_BM_PASS'))

    # Espera 1 segundo
    time.sleep(1)

    # Encuentra el botón de tipo "submit" y haz clic en él
    submit_button = driver.find_element(By.XPATH, "/html/body/app-root/app-landing-page/section/div/div/div/app-login-empleador/div/form/button")
    
    submit_button.click()

    # Espera hasta que el elemento <strong> esté presente
    try:
        wait = WebDriverWait(driver, 40)
        keyword = "ISAPRE BANMEDICA S.A."
        xpath = f"//*[@id='cont_home']/div[1]/div[2]/div/table/tbody/tr[1]/td/span[contains(text(), '{keyword}')]"
        greeting_element = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Imprime el texto del elemento identificado
        # print(f"Texto encontrado: {greeting_element.text}")

        if keyword in greeting_element.text:
            print(f"0: texto [{keyword}] encontrado ")
        else:
            print(f"2: texto no [{keyword}] encontrado ")
    except Exception as e:
        print(f"2: Excepción al validar texto [{keyword}]: {e}")
        
finally:
    # Cierra el navegador
    driver.quit()
    #print("Terminado")
