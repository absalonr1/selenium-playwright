from playwright.sync_api import sync_playwright
import time
import os

def login_with_playwright():
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(http_credentials={
                'username': os.getenv('LOGIN_CRM_USER'),
                'password': os.getenv('LOGIN_CRM_PASS')
            },
            viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()
            #page.goto("https://crmsts.banmedica.cl/adfs/ls/wia?wa=wsignin1.0&wtrealm=https%3a%2f%2fcrm.banmedica.cl%2f&wctx=rm%3d1%26id%3df8427922-ce04-4b94-be27-db04d5d9bc8c%26ru%3d%252fdefault.aspx%26crmorgid%3d00000000-0000-0000-0000-000000000000&wct=2024-12-21T21%3a31%3a40Z&wauth=urn%3afederation%3aauthentication%3awindows&client-request-id=d794c2bb-f230-4faf-3835-0380030000d7")
            page.goto("https://crm.banmedica.cl")
            # page.wait_for_load_state("load")  # "load", "domcontentloaded", o "networkidle"


            # Selector XPath del elemento
            selector = '//*[@id="userInformationLauncher_buttoncrm_header_global_me-control"]/button/span/span/span'

            page.wait_for_selector(selector, timeout=5000)

            # Verificar si el elemento existe
            try:
                element = page.locator(selector)

                if element.is_visible():
                    print(f"0: El elemento existe y es visible [classs: '{element.get_attribute("class")}']")
                else:
                    print("0: El elemento existe pero no es visible.")
            except Exception as e:
                print("2: El elemento no existe:", str(e))
            
            #time.sleep(20)
        finally:
            browser.close()

login_with_playwright()
