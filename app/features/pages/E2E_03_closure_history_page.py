from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from features.utils.tickets_store import load_ticket
class ClosureHistoryPage(BasePage):
    HISTORIAL_CIERRES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Cierres")')
    def __init__(self, driver):
        super().__init__(driver)
    def open_closure_history(self):
        self.click(self.HISTORIAL_CIERRES)
    def verify_closure_history(self):
        saved_closure = load_ticket()
        if not saved_closure:
            raise AssertionError("No se encontró ningún cierre guardado en tmp/last_ticket.json")
        expected_datetime = saved_closure.get("date")
        expected_amount = saved_closure.get("amount")
        print(f"Cierre guardado: {saved_closure!r}")
        print(f"Fecha buscada: {expected_datetime!r}")
        print(f"Importe buscado: {expected_amount!r}")
        if not expected_datetime:
            raise AssertionError("El cierre guardado no contiene fecha")
        if not expected_amount:
            raise AssertionError("El cierre guardado no contiene importe")
        return self.find_closure(expected_datetime, expected_amount)
    def find_closure(self, expected_datetime, expected_amount):
        expected_datetime = expected_datetime.strip()
        expected_amount = expected_amount.strip()
        print(f"Buscando fecha: {expected_datetime!r}")
        print(f"Buscando importe: {expected_amount!r}")
        date_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{expected_datetime}")')
        date_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(date_locator))
        print(f"Fecha encontrada: {date_element.text!r}")
        amount_elements = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{expected_amount}")')
        print(f"Importes encontrados: {len(amount_elements)}")
        for amount_element in amount_elements:
            print(f"Importe encontrado: {amount_element.text!r}")
            date_rect = date_element.rect
            amount_rect = amount_element.rect
            if abs(date_rect["y"] - amount_rect["y"]) < 50:
                print("Cierre encontrado correctamente")
                print("Fecha e importe pertenecen a la misma fila")
                return True
        print(f"No se encontró el cierre esperado: fecha={expected_datetime!r}, importe={expected_amount!r}")
        return False
