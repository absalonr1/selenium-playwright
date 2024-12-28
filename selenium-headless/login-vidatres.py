from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

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
    url = "https://login.isaprevidatres.cl/login"
    driver.get(url)

    # Espera para asegurarse de que la página cargue
    time.sleep(5)

   # Encuentra el campo con ID "rut" y escribe "1"
    rut_field = driver.find_element(By.ID, "rut")
    rut_field.send_keys(os.getenv('LOGIN_VT_USER'))

    # Encuentra el campo con ID "current-password" y escribe "2"
    password_field = driver.find_element(By.ID, "current-password")
    password_field.send_keys(os.getenv('LOGIN_VT_PASS'))

    # Espera 1 segundo
    time.sleep(1)

    # Encuentra el botón de tipo "submit" y haz clic en él
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary')]")
    submit_button.click()

    # Espera hasta que el elemento <strong> esté presente
    try:
        wait = WebDriverWait(driver, 40)
        greeting_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='btn-user']/span/small[contains(text(),'Aaron Stefano')]"))
        )

        # Imprime el texto del elemento identificado
        # print(f"Texto encontrado: {greeting_element.text}")

        if greeting_element.text == "Aaron Stefano":
            print("0: texto [Aaron Stefano] encontrado ")
        else:
            print("2: texto no [Aaron Stefano] encontrado ")
    except Exception as e:
        print(f"2: Excepción al validar texto [Aaron Stefano]: {e}")
        
finally:
    # Cierra el navegador
    driver.quit()
    #print("Terminado")
