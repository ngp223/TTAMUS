import time
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.tickets_history_store import load_ticket_history


class TicketsHistoryPage(BasePage):
    HISTORIAL_TICKETS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Historial de Tickets")')
    FECHA_PRIMER_TICKET = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-tickets-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-2")')
    IMPORTE_PRIMER_TICKET = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-historial-tickets-page-1-tam-card-tam-card-1-div-tbody-1-div-row-1-span-col-3")')

    def __init__(self, driver):
        super().__init__(driver)

    def open_tickets_history(self):
        self.click(self.HISTORIAL_TICKETS)

    def verify_tickets_history(self):
        saved_ticket = load_ticket_history()
        if not saved_ticket:
            print("ERROR: No existe ningún ticket guardado para comprobar el historial")
            return False
        print(f"Ticket guardado: {saved_ticket!r}")
        return self.find_ticket(saved_ticket["date"], saved_ticket["amount"])

    def find_ticket(self, expected_date, expected_amount):
        try:
            time.sleep(3)
            fecha = self.driver.find_element(*self.FECHA_PRIMER_TICKET).text.strip()
            importe = self.driver.find_element(*self.IMPORTE_PRIMER_TICKET).text.strip()
            print(f"Fecha encontrada: {fecha!r}")
            print(f"Importe encontrado: {importe!r}")
            print(f"Fecha esperada: {expected_date!r}")
            print(f"Importe esperado: {expected_amount!r}")
            if fecha == expected_date and importe == expected_amount:
                print("Ticket encontrado correctamente en la primera fila")
                return True
            print("ERROR: La fecha o el importe no coinciden con el ticket guardado")
            return False
        except Exception as e:
            print(f"ERROR al localizar la primera fila del historial: {e}")
            print(f"Contexto Appium: {self.driver.current_context}")
            return False