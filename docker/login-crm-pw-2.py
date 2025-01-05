from playwright.sync_api import sync_playwright
import time
import os
import logging


logging.basicConfig(
    filename=os.getenv("LOG_FILE"),       # Archivo donde se guardarán los logs
    level=logging.INFO,                     # Nivel de los logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Formato del mensaje
    datefmt='%Y-%m-%d %H:%M:%S'                         # Formato de fecha y hora
)

global flagFound
flagFound = False
def login_with_playwright():
    with sync_playwright() as p:
        try:
            url = "https://crm.banmedica.cl"

            headless = bool(os.getenv('HEADLESS'))
            
            browser = p.firefox.launch(headless=headless)
            context = browser.new_context(
                http_credentials={
                    'username': os.getenv('LOGIN_CRM_USER'),
                    'password': os.getenv('LOGIN_CRM_PASS')
                },
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            # Define el manejo del diálogo (pop-up)
            def handle_dialog(dialog):
                print("Interceptado el pop-up de autenticación.")
                username = os.getenv("LOGIN_CRM_USER")
                password = os.getenv("LOGIN_CRM_PASS")
                dialog.accept(f"{username}\n{password}")  # Formato esperado: "usuario\ncontraseña"

            page.on("dialog", handle_dialog)
                        
            def log_response(response):
                logging.info(f"Respuesta recibida: {response.url} - Estado: {response.status}")
                global flagFound
                #https://crm.banmedica.cl/CRMClientes/main.aspx?forceUCI=1&appid=a31e9d38-e45b-4542-862d-1041e65ec18d
                #https://crm.banmedica.cl/CRMClientes/default.aspx
                if response.status == 200 and response.url == "https://crm.banmedica.cl/CRMClientes/main.aspx?forceUCI=1&appid=a31e9d38-e45b-4542-862d-1041e65ec18d":
                    
                    flagFound = True
                    print(f"0: Prueba OK. [https://crm.banmedica.cl/CRMClientes/main.aspx?forceUCI=1&appid=a31e9d38-e45b-4542-862d-1041e65ec18d] ")
                    
                    #exit(0)  

            page.on("response", log_response)

            page.goto(url, wait_until="load")
            
            
            page.wait_for_url("https://crm.banmedica.cl/CRMClientes/main.aspx?forceUCI=1&appid=a31e9d38-e45b-4542-862d-1041e65ec18d", timeout=10000,wait_until='load')
            #print("Listo")
            time.sleep(5)
            if not flagFound:
                print(f"0: Prueba NO OK. [https://crm.banmedica.cl/CRMClientes/main.aspx?forceUCI=1&appid=a31e9d38-e45b-4542-862d-1041e65ec18d] ")

        except Exception as e:
            print(f"2: Excepcion al validar elemento [{url}]")
            logging.error(f"2: Excepcion al validar elemento.{e}")
        finally:
            browser.close()

login_with_playwright()
