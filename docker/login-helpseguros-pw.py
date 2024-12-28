from playwright.sync_api import sync_playwright
import os
import time

def main():
    with sync_playwright() as p:
        # Configurar el navegador en modo headless con ajustes avanzados
        browser = p.firefox.launch(
            headless=True, 
            args=["--window-size=1024,780", "--disable-blink-features=AutomationControlled"]
        )
        
        # Configuración del contexto del navegador
        context = browser.new_context(
            viewport={"width": 1024, "height": 780},  # Tamaño de ventana
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        
        # Crear una nueva página
        page = browser.new_page()
        
        # Navegar a la URL
        keyword = "Johan"
        url = "https://login.helpseguros.cl/login"
        page.goto(url)

        #time.sleep(2)
        # Rellenar el formulario
        try:
            # Esperar a que los campos estén disponibles y rellenarlos
            page.wait_for_selector("#rut", state="visible")
            page.fill("#rut", os.getenv('LOGIN_HELP_USER'))

            #time.sleep(2)

            page.wait_for_selector("#current-password", state="visible")
            page.fill("#current-password", os.getenv('LOGIN_HELP_PASS'))

            
            # Hacer clic en el botón de "submit"
            submit_button_selector = "#btnIngresar"
            page.wait_for_selector(submit_button_selector, state="visible")
            page.click(submit_button_selector)

            element = page.wait_for_selector("iframe#pandoraBox", timeout=10000)
            print("Loaded iframe: " + str(element.get_attribute("src")))
            iframe_locator = page.frame_locator("iframe#pandoraBox")

            # Esperar hasta que el elemento <strong> esté disponible
            #
            #//*[@id='iosfix']/app-home/div/div[1]/div[1]/div/div/div[1]/div/h2/span[1]/strong
            xpath = f"//html/body/app-root/div/app-home/div/div[1]/div[1]/div/div/div[1]/div/h2/span[1]/strong[contains(text(), '{keyword}')]"
            
            # Esperar hasta que el elemento esté visible
            print ("esperando por el keyword")
            iframe_locator.locator(f"xpath={xpath}").wait_for(state="visible", timeout=10000)
            
            element_text = iframe_locator.locator(xpath).inner_text()
            if keyword in element_text:
                print(f"0: texto [{keyword}] encontrado ")
                time.sleep(2)
                screenshot_path = "lastrun/login-help.png"
                page.screenshot(path=screenshot_path)
            else:
                print(f"2: texto [{keyword}] no encontrado ")
        except Exception as e:
            # Capturar una captura de pantalla para depurar
            page.screenshot(path="lastrun/login-help_debug_error.png")
            print(f"2: Excepción al validar texto [{keyword}]: {e}")
        finally:
            # Cerrar el navegador
            browser.close()

# Ejecutar el script
if __name__ == "__main__":
    main()
