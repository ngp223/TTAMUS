from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT
import time


class ReservationPage(BasePage):
    RESERVATIONS_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reservas")')
    RESERVATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva reserva")')
    NAME = (AppiumBy.CSS_SELECTOR, "input#reservation-name")
    SEARCH_RESERVATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("reservations-search")')
    SAVE_RESERVATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Guardar reserva")')
    RECORD_ARRIVAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Marcar llegada")')
    OPTIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-listbody-1-section-day-1-div-day__items-1-article-item-1-div-item__actions-1-button-tam-btn-2")')
    OPTIONS_SEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-listbody-1-section-day-1-div-day__items-1-article-item-1-div-item__actions-1-button-tam-btn-1")')
    EDIT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')
    CANCEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cancelar")')
    NO_RESERVATIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No hay reservas")')
    DINERS = (AppiumBy.CSS_SELECTOR, "input#reservation-party-size")
    RESERVATION_LOCATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{}")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_reservation = None

    def access_reservation(self):
        self.click(self.RESERVATIONS_MENU)

    def create_reservation(self):
        self.click(self.RESERVATION)
        date_time = datetime.now().strftime('%H%M%S%d%m%Y')
        self.created_reservation = f"ClienteQA_{date_time}"
        self.write_webview(self.NAME, self.created_reservation, timeout=WAIT_TIMEOUT)
        self.click(self.SAVE_RESERVATION)

    def search_reservation(self):
        if not self.created_reservation:
            raise Exception("No existe reserva creada para comprobar")
        search_field = self.wait_visibility(self.SEARCH_RESERVATION, timeout=WAIT_TIMEOUT)
        search_field.click()
        search_field.clear()
        search_field.send_keys(self.created_reservation)
        reservation_locator = (self.RESERVATION_LOCATOR[0], self.RESERVATION_LOCATOR[1].format(self.created_reservation))
        self.wait_visibility(reservation_locator, timeout=WAIT_TIMEOUT)

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
