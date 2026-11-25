from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT


class ReservationPage(BasePage):
    RESERVATIONS_MENU = BasePage.by_text("Reservas")
    RESERVATION = BasePage.by_text("Nueva reserva")
    NAME = (AppiumBy.CSS_SELECTOR, "input#reservation-name")
    SEARCH_RESERVATION = BasePage.by_id("reservations-search")
    SAVE_RESERVATION = BasePage.by_text("Guardar reserva")
    RECORD_ARRIVAL = BasePage.by_text("Marcar llegada")
    OPTIONS = BasePage.by_id("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-listbody-1-section-day-1-div-day__items-1-article-item-1-div-item__actions-1-button-tam-btn-2")
    OPTIONS_SEL = BasePage.by_id("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-listbody-1-section-day-1-div-day__items-1-article-item-1-div-item__actions-1-button-tam-btn-1")
    EDIT = BasePage.by_text("Editar")
    CANCEL = BasePage.by_text("Cancelar")
    NO_RESERVATIONS = BasePage.by_text("No hay reservas")
    DINERS = (AppiumBy.CSS_SELECTOR, "input#reservation-party-size")

    def __init__(self, driver):
        super().__init__(driver)
        self.created_reservation = None

    def access_reservation(self):
        self.click(self.RESERVATIONS_MENU)

    def create_reservation(self):
        self.click(self.RESERVATION)
        self.created_reservation = f"ClienteQA_{datetime.now().strftime('%H%M%S%d%m%Y')}"
        self.write_webview(self.NAME, self.created_reservation, timeout=WAIT_TIMEOUT)
        self.click(self.SAVE_RESERVATION)

    def search_reservation(self):
        if not self.created_reservation:
            raise Exception("No existe reserva creada para comprobar")
        self.search_and_find(self.SEARCH_RESERVATION, self.created_reservation, timeout=WAIT_TIMEOUT)

    def check_reservation(self):
        self.click(self.RECORD_ARRIVAL)

    def edit_reservation(self):
        self.click(self.OPTIONS)
        self.click(self.EDIT)
        self.write_webview(self.DINERS, "3", timeout=WAIT_TIMEOUT)
        self.click(self.SAVE_RESERVATION)

    def cancel_reservation(self):
        self.click(self.OPTIONS_SEL)
        self.click(self.CANCEL)

    def verify_cancel_reservation(self):
        if not self.created_reservation:
            raise Exception("No existe reserva creada para comprobar")
        self.wait_visibility(self.NO_RESERVATIONS, timeout=WAIT_TIMEOUT)