from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from features.utils.save_load_files import save_ticket_history
from datetime import datetime
import re


class CashClosurePage(BasePage):
    CASH_CLOSURE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cierre de Caja")')
    FINALIZE_CLOSURE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Realizar Cierre")')
    STAY_CONNECTED = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-cancel")')
    LOGIN_USER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)

    def open_cash_closure(self):
        self.click(self.CASH_CLOSURE_BUTTON)

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
        self.click(self.FINALIZE_CLOSURE)
        self.click(self.STAY_CONNECTED)
        save_ticket_history(context.last_closure_date, context.last_closure_amount)
        print("Ticket guardado correctamente")

