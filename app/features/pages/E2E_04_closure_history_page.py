
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from features.utils.save_load_files import load_ticket_history
from features.config.test_config import WAIT_TIMEOUT
from datetime import datetime
import time


class ClosureHistoryPage(BasePage):
    CLOSING_HISTORY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Cierres")')
    DATE_FIRST_CLOSURE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-cierres-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-4")')
    AMOUNT_FIRST_CLOSURE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-cierres-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-6")')

    def __init__(self, driver):
        super().__init__(driver)

    def open_closure_history(self):
        self.click(self.CLOSING_HISTORY)

    def verify_closure_history(self):
        saved_closure = load_ticket_history()
        if not saved_closure:
            raise AssertionError("No existe ningún cierre guardado para comprobar el historial")
        print(f"Cierre guardado: {saved_closure!r}")
        assert self.find_closure(saved_closure["date"], saved_closure["amount"]), "No se encontró el cierre esperado en el historial"

    def find_closure(self, expected_date, expected_amount):
        time.sleep(3)
        try:
            WebDriverWait(self.driver, WAIT_TIMEOUT).until(EC.visibility_of_element_located(self.DATE_FIRST_CLOSURE))
            actual_date = self.driver.find_element(*self.DATE_FIRST_CLOSURE).text.strip()
            actual_amount = self.driver.find_element(*self.AMOUNT_FIRST_CLOSURE).text.strip()
            print(f"Fecha encontrada: '{actual_date}' | esperada: '{expected_date}'")
            if actual_amount != expected_amount.strip():
                return False
            actual = datetime.strptime(actual_date, "%d/%m/%Y, %H:%M")
            expected = datetime.strptime(expected_date.strip(), "%d/%m/%Y, %H:%M")
            diferencia = abs((actual - expected).total_seconds())
            return diferencia <= 60
        except Exception as e:
            print(f"Error al buscar el cierre: {type(e).__name__}: {e}")
            return False

