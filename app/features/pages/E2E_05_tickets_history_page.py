import time
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.tickets_store import load_ticket


class TicketsHistoryPage(BasePage):
    TICKET_HISTORY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Tickets")')
    DATE_FIRST_TICKET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-tickets-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-2")')
    AMOUNT_FIRST_TICKET = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-tickets-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-3")')

    def __init__(self, driver):
        super().__init__(driver)

    def open_tickets_history(self):
        self.click(self.TICKET_HISTORY)

    def verify_tickets_history(self):
        saved_ticket = load_ticket()
        if not saved_ticket:
            raise AssertionError("No existe ningún ticket guardado para comprobar el historial")
        print(f"Ticket guardado: {saved_ticket!r}")
        assert self.find_ticket(saved_ticket["date"], saved_ticket["amount"]), "No se encontró el ticket esperado en el historial"

    def find_ticket(self, expected_date, expected_amount):
        try:
            time.sleep(3)
            date = self.driver.find_element(*self.DATE_FIRST_TICKET).text.strip()
            amount = self.driver.find_element(*self.AMOUNT_FIRST_TICKET).text.strip()
            print(f"Fecha encontrada: {date!r}")
            print(f"Importe encontrado: {amount!r}")
            print(f"Fecha esperada: {expected_date!r}")
            print(f"Importe esperado: {expected_amount!r}")
            if date == expected_date and amount == expected_amount:
                print("Ticket encontrado correctamente en la primera fila")
                return True
            print("ERROR: La fecha o el importe no coinciden con el ticket guardado")
            return False
        except Exception as e:
            print(f"ERROR al localizar la primera fila del historial: {e}")
            print(f"Contexto Appium: {self.driver.current_context}")
            return False
