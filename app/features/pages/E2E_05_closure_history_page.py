from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.save_load_files import load_ticket_history
from features.config.test_config import WAIT_TIMEOUT


class ClosureHistoryPage(BasePage):
    CLOSING_HISTORY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Cierres")')
    DATE_FIRST_CLOSURE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-cierres-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-4")')
    AMOUNT_FIRST_CLOSURE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-cierres-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-6")')

    def open_closure_history(self):
        self.click(self.CLOSING_HISTORY)

    def verify_closure_history(self):
        saved_closure = load_ticket_history()
        if not saved_closure:
            raise AssertionError("No existe ningún cierre guardado para comprobar el historial")
        print(f"Cierre guardado: {saved_closure!r}")
        if not self.find_closure(saved_closure["date"], saved_closure["amount"]):
            raise AssertionError("No se encontró el cierre esperado en el historial")

    def find_closure(self, expected_date, expected_amount):
        return self.wait_date_amount_match(self.DATE_FIRST_CLOSURE, self.AMOUNT_FIRST_CLOSURE, expected_date, expected_amount, timeout=WAIT_TIMEOUT)