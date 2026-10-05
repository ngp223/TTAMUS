from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage

class ReservationPage(BasePage):
    RESERVAS_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reservas")')
    CLIENTE = (AppiumBy.XPATH, '//*[@resource-id="tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-reservations-page-1-div-layout-1-tam-card-tam-card-1-div-formcard__scroll-1-div-grid-1-div-field-1-tam-input-tam-input-1-div-tam-input__wrap-1"]')
    GUARDAR_RESERVA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Guardar reserva")')
    BUSCAR_RESERVAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')

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