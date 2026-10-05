from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
import time

class ReservationPage(BasePage):
    RESERVAS_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reservas")')
    CLIENTE = (AppiumBy.XPATH, '//*[@resource-id="tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-formcard__scroll-1-div-grid-1-div-field-1-tam-input-tam-input-1-div-tam-input__wrap-1"]')
    GUARDAR_RESERVA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Guardar reserva")')
    BUSCAR_RESERVAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    MARCAR_LLEGADA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-2-div-listbody-1-article-item-1-div-item__bottom-1-div-item__actions-1-button-tam-btn-2")')
    CANCELAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-2-div-listbody-1-article-item-1-div-item__bottom-1-div-item__actions-1-button-tam-btn-3")')
    NO_HAY_RESERVAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("No hay reservas")')

    def __init__(self, driver):
        super().__init__(driver)
        self.reserva_creada = None

    def acceder_reservas(self):
        self.click(self.RESERVAS_MENU)

    def crear_reserva(self):
        fecha_hora = datetime.now().strftime('%d%m%Y%H%M%S')
        self.reserva_creada = f"ClienteQA_{fecha_hora}"
        self.escribir_valor(self.CLIENTE, self.reserva_creada)
        self.click(self.GUARDAR_RESERVA)

    def comprobar_reserva_creada(self):
        if not self.reserva_creada:
            raise Exception("No existe reserva creada para comprobar")
        self.escribir(self.BUSCAR_RESERVAS, self.reserva_creada)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass
        locator_reserva = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.reserva_creada}")')
        self.esperar_visible(locator_reserva, timeout=15)

    def buscar_reserva(self):
        if not self.reserva_creada:
            raise Exception("No existe reserva creada para buscar")
        self.escribir(self.BUSCAR_RESERVAS, self.reserva_creada)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def localizar_reserva(self):
        self.buscar_reserva()
        locator_reserva = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.reserva_creada}")')
        return self.esperar_visible(locator_reserva, timeout=15)

    def localizar_accion_reserva(self, locator):
        reserva = self.localizar_reserva()
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

    def marcar_reserva_como_llegada(self):
        elemento_marcar = self.localizar_accion_reserva(self.MARCAR_LLEGADA)
        elemento_marcar.click()

    def cancelar_reserva(self):
        elemento_cancelar = self.localizar_accion_reserva(self.CANCELAR)
        elemento_cancelar.click()

    def comprobar_reserva_cancelada(self):
        if not self.reserva_creada:
            raise Exception("No existe reserva creada para comprobar")
        self.buscar_reserva()
        time.sleep(2)
        self.esperar_visible(self.NO_HAY_RESERVAS, timeout=10)