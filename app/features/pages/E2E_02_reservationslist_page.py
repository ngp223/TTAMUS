
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT
import time


class ReservationPage(BasePage):
    RESERVATIONS_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reservas")')
    CUSTOMER = (AppiumBy.XPATH, '//*[@resource-id="tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-formcard__scroll-1-div-grid-1-div-field-1-tam-input-tam-input-1-div-tam-input__wrap-1"]')
    SAVE_RESERVATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Guardar reserva")')
    SEARCH_RESERVATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    RECORD_ARRIVAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-2-div-listbody-1-article-item-1-div-item__bottom-1-div-item__actions-1-button-tam-btn-2")')
    CANCEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-2-div-listbody-1-article-item-1-div-item__bottom-1-div-item__actions-1-button-tam-btn-3")')
    NO_RESERVATIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No hay reservas")')
    EDIT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')
    DINERS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-6")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_reservation = None

    def access_reservation(self):
        self.click(self.RESERVATIONS_MENU)

    def create_reservation(self):
        date_time = datetime.now().strftime('%d%m%Y%H%M%S')
        self.created_reservation = f"ClienteQA_{date_time}"
        self.value_write(self.CUSTOMER, self.created_reservation)
        self.click(self.SAVE_RESERVATION)

    def verify_create_reservation(self):
        if not self.created_reservation:
            raise Exception("No existe reserva creada para comprobar")
        self.write(self.SEARCH_RESERVATION, self.created_reservation)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        reservation_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_reservation}")')
        self.wait_visibility(reservation_locator, timeout=WAIT_TIMEOUT)

    def search_reservation(self):
        if not self.created_reservation:
            raise Exception("No existe reserva creada para buscar")
        self.write(self.SEARCH_RESERVATION, self.created_reservation)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def find_reservation(self):
        self.search_reservation()
        reservation_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_reservation}")')
        return self.wait_visibility(reservation_locator, timeout=WAIT_TIMEOUT)

    def find_reservation_action(self, locator):
        reservation = self.find_reservation()
        reservation_y = reservation.location["y"]
        elements = self.driver.find_elements(*locator)
        if not elements:
            raise Exception(f"No se encontraron elementos para la acción: {locator}")
        correct_element = None
        minimum_distance = float("inf")
        for element in elements:
            if not element.is_displayed():
                continue
            distance = abs(element.location["y"] - reservation_y)
            if distance < minimum_distance:
                minimum_distance = distance
                correct_element = element
        if correct_element is None:
            raise Exception(f"No se encontró la acción para la reserva {self.created_reservation}")
        return correct_element

    def check_reservation(self):
        arrival_element = self.find_reservation_action(self.RECORD_ARRIVAL)
        arrival_element.click()

    def edit_reservation(self):
        self.find_reservation()
        self.click(self.EDIT)
        diners_field = self.wait_visibility(self.DINERS, timeout=WAIT_TIMEOUT)
        diners_field.clear()
        self.value_write(self.DINERS, "3")
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        self.click(self.SAVE_RESERVATION)

    def cancel_reservation(self):
        cancel_element = self.find_reservation_action(self.CANCEL)
        cancel_element.click()

    def verify_cancel_reservation(self):
        if not self.created_reservation:
            raise Exception("No existe reserva creada para comprobar")
        self.find_reservation()
        time.sleep(2)
        self.wait_visibility(self.NO_RESERVATIONS, timeout=WAIT_TIMEOUT)
