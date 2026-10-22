from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from features.utils.tickets_history_store import save_ticket_history
from datetime import datetime
import re

class CashClosurePage(BasePage):
    CASH_CLOSURE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cierre de Caja")')
    DECLARED_SECTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("visibility Normal Declarado Ver esperado y declarar contado")')
    COPY_EXPECTED_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copiar esperado").instance(0)')
    COPY_EXPECTED_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copiar esperado").instance(1)')
    FINALIZE_CLOSURE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Realizar Cierre")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)

    def open_cash_closure(self):
        self.click(self.CASH_CLOSURE_BUTTON)

    def open_declared_section(self):
        self.mobile_utils.swipe_up()
        self.click(self.DECLARED_SECTION)

    def copy_expected_first(self):
        self.click(self.COPY_EXPECTED_1)

    def copy_expected_second(self):
        self.click(self.COPY_EXPECTED_2)

    def scroll_to_finalize(self):
        self.mobile_utils.swipe_up()

    def get_closure_total(self):
        end_time = __import__("time").time() + 10

        while __import__("time").time() < end_time:
            elements = self.driver.find_elements(AppiumBy.XPATH, '//*[contains(@text,"€")]')

            for element in elements:
                try:
                    text = element.text.strip()

                    if re.fullmatch(r'\d{1,3}(?:\.\d{3})*,\d{2}\s*€', text):
                        print(f"Importe cierre encontrado: {text}")
                        return text

                except Exception:
                    continue

            __import__("time").sleep(0.5)

        raise Exception("No se encontró ningún importe con € en el cierre de caja")

    def complete_cash_closure(self, context):
        context.last_closure_date = datetime.now().strftime("%d/%m/%Y, %H:%M")
        context.last_closure_amount = self.get_closure_total()
        print(f"Fecha cierre: {context.last_closure_date}")
        print(f"Importe cierre: {context.last_closure_amount}")
        self.finalize_closure()
        save_ticket_history(context.last_closure_date, context.last_closure_amount)
        print("Ticket guardado correctamente")

    def finalize_closure(self):
        self.click(self.FINALIZE_CLOSURE)
