import requests
import sys
import os

def get_initial_cookie():
    """
    Obtiene la cookie inicial del sitio web.
    """
    try:
        url = "https://vsp.banmedica.cl/"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Imprimir cookies obtenidas
            print("Cookies iniciales:", response.cookies, file=sys.stdout)
            # Retornar las cookies obtenidas
            return response.cookies.get_dict()
        else:
            print("2: Error al obtener la cookie inicial", file=sys.stdout)
            sys.exit(2)
    except Exception as e:
        print(f"2: Excepción al obtener la cookie inicial: {e}", file=sys.stdout)
        sys.exit(2)

def perform_login(cookie):
    """
    Realiza el login y verifica el atributo Int1 en el JSON retornado.
    """
    try:
        url = "https://vsp.banmedica.cl/Autenticacion/ValidarUsuarioBansecurity"
        params = {
            "username": os.getenv('LOGIN_VSP_USER'),
            "pass": os.getenv('LOGIN_VSP_PASS'),
            "tipoDevice": "Mac",
            "sistemaOperativo": "Windows",
            "navegador": "Mobile Safari",
            "_": "1733418015276"
        }
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,es;q=0.8,ca;q=0.7",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": "https://vsp.banmedica.cl/",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

        response = requests.get(url, headers=headers, cookies=cookie, params=params)

        # Imprimir cookies de la respuesta
        print("Cookies de la respuesta del login:", response.cookies, file=sys.stdout)

        # Validar respuesta
        if response.status_code == 200:
            response_json = response.json()
            if str(response_json.get("Int1")) == "16746695":
                print("Login exitoso: Atributo Int1 encontrado", file=sys.stdout)
                return response.cookies.get_dict()
            else:
                print(f"2: Login fallido, Int1 no coincide. Respuesta JSON: {response_json}", file=sys.stdout)
                sys.exit(2)
        else:
            print(f"2: Error en el login. Código de estado: {response.status_code}", file=sys.stdout)
            sys.exit(2)
    except Exception as e:
        print(f"2: Excepción durante el login: {e}", file=sys.stdout)
        sys.exit(2)

def validate_final_page(cookie):
    """
    Realiza el GET a la URL final y verifica si existe la frase "Aaron Valenzuela Cecchi" en el HTML.
    """
    try:
        url = "https://vsp.banmedica.cl/Inicio/Inicio"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers, cookies=cookie)

        # Validar respuesta
        print(response.text)
        if response.status_code == 200:
            if "Aaron Valenzuela Cecchi" in response.text:
                print("0: Test exitoso: Frase encontrada en la página final", file=sys.stdout)
                sys.exit(0)
            else:
                print("2: Test fallido: Frase no encontrada en la página final", file=sys.stdout)
                sys.exit(2)
        else:
            print(f"2: Error al acceder a la página final. Código de estado: {response.status_code}", file=sys.stdout)
            sys.exit(2)
    except Exception as e:
        print(f"2: Excepción al validar la página final: {e}", file=sys.stdout)
        sys.exit(2)

if __name__ == "__main__":
    # Paso 1: Obtener la cookie inicial
    initial_cookie = get_initial_cookie()

    # Paso 2: Realizar el login y obtener las cookies del login
    login_cookie = perform_login(initial_cookie)

    # Paso 3: Validar la página final con las cookies obtenidas
    validate_final_page(initial_cookie)
