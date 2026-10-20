from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
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
        self.reserva_creada = None

    def access_reservation(self):
        self.click(self.RESERVATIONS_MENU)

    def create_reservation(self):
        fecha_hora = datetime.now().strftime('%d%m%Y%H%M%S')
        self.reserva_creada = f"ClienteQA_{fecha_hora}"
        self.value_write(self.CUSTOMER, self.reserva_creada)
        self.click(self.SAVE_RESERVATION)

    def verify_create_reservation(self):
        if not self.reserva_creada:
            raise Exception("No existe reserva creada para comprobar")
        self.write(self.SEARCH_RESERVATION, self.reserva_creada)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        locator_reserva = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.reserva_creada}")')
        self.wait_visibility(locator_reserva, timeout=15)

    def search_reservation(self):
        if not self.reserva_creada:
            raise Exception("No existe reserva creada para buscar")
        self.write(self.SEARCH_RESERVATION, self.reserva_creada)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def find_reservation(self):
        self.search_reservation()
        locator_reserva = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.reserva_creada}")')
        return self.wait_visibility(locator_reserva, timeout=15)

    def localizar_accion_reserva(self, locator):
        reserva = self.find_reservation()
        reserva_y = reserva.location["y"]
        elementos = self.driver.find_elements(*locator)
        if not elementos:
            raise Exception(f"No se encontraron elementos para la acción: {locator}")
        elemento_correcto = None
        distancia_minima = float("inf")
        for elemento in elementos:
            if not elemento.is_displayed():
                continue
            distancia = abs(elemento.location["y"] - reserva_y)
            if distancia < distancia_minima:
                distancia_minima = distancia
                elemento_correcto = elemento
        if elemento_correcto is None:
            raise Exception(f"No se encontró la acción para la reserva {self.reserva_creada}")
        return elemento_correcto

    def check_reservation(self):
        elemento_marcar = self.localizar_accion_reserva(self.RECORD_ARRIVAL)
        elemento_marcar.click()

    def edit_reservation(self):
        self.find_reservation()
        self.click(self.EDIT)
        campo = self.wait_visibility(self.DINERS, timeout=15)
        campo.clear()
        self.value_write(self.DINERS, "3")
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        self.click(self.SAVE_RESERVATION)
        
    def cancel_reservation(self):
        elemento_cancel = self.localizar_accion_reserva(self.CANCEL)
        elemento_cancel.click()

    def verify_cancel_reservation(self):
        if not self.reserva_creada:
            raise Exception("No existe reserva creada para comprobar")
        self.find_reservation()
        time.sleep(2)
        self.wait_visibility(self.NO_RESERVATIONS, timeout=10)