from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.save_load_files import load_ticket
from features.config.test_config import WAIT_TIMEOUT


class TicketsHistoryPage(BasePage):
    TICKET_HISTORY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Tickets")')
    DATE_FIRST_TICKET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-tickets-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-2")')
    AMOUNT_FIRST_TICKET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-tickets-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-3")')

    def open_tickets_history(self):
        self.click(self.TICKET_HISTORY)

    def verify_tickets_history(self):
        saved_ticket = load_ticket()
        if not saved_ticket:
            raise AssertionError("No existe ningún ticket guardado para comprobar el historial")
        print(f"Ticket guardado: {saved_ticket!r}")
        if not self.find_ticket(saved_ticket["date"], saved_ticket["amount"]):
            raise AssertionError("No se encontró el ticket esperado en el historial")

    def find_ticket(self, expected_date, expected_amount):
        return self.wait_date_amount_match(self.DATE_FIRST_TICKET, self.AMOUNT_FIRST_TICKET, expected_date, expected_amount, timeout=WAIT_TIMEOUT)