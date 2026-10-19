
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.tickets_history_store import save_ticket_history
from datetime import datetime
import time


class ReservationPage(BasePage):
    VISTA_MESAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Vista de mesas")')
    SALON_PRINCIPAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salón principal")')
    MESA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAL-04")')
    COMENSALES_3 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("3")')
    ACEPTAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Aceptar")')
    CARNES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Carnes")')
    SOLOMILLO_FOIE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Con opciones Solomillo al foie 24,50 €")')
    VERDURAS_PLANCHA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("radio_button_unchecked Verduras a la plancha")')
    POCO_HECHO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("radio_button_unchecked Poco hecho")')
    AÑADIR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Añadir")')
    ARROCES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Arroces")')
    RISOTTO_SETAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Risotto de setas 15,50 €")')
    ENVIAR_A_COCINA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enviar a cocina")')
    AUMENTAR_PRODUCTO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("＋")')
    COBRAR_40 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cobrar 64,50 €")')
    BOTON_COBRAR = (AppiumBy.ID, "tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-sales-view-1-tam-payment-view-fill-1-div-pay-1-tam-card-tam-card-2-div-pay__actions-1-button-tam-btn-2")
    MESA_LIBERADA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Mesa liberada")')

    def __init__(self, driver):
        super().__init__(driver)

    def access_see_tables(self):
        return self.esperar_visible(self.VISTA_MESAS)

    def select_table(self):
        self.click(self.SALON_PRINCIPAL)
        self.esperar_visible(self.MESA)
        self.click(self.MESA)
        time.sleep(2)

    def select_guests(self):
        self.click(self.COMENSALES_3)

    def click_accept_guests(self):
        self.click(self.ACEPTAR)

    def select_product(self):
        self.click(self.CARNES)
        self.click(self.SOLOMILLO_FOIE)
        self.click(self.VERDURAS_PLANCHA)
        self.click(self.POCO_HECHO)
        self.click(self.AÑADIR)
        self.click(self.ARROCES)
        self.click(self.RISOTTO_SETAS)

    def increase_product(self):
        self.click(self.AUMENTAR_PRODUCTO)

    def save_ticket_data(self):
        try:
            button = self.driver.find_element(*self.BOTON_COBRAR)
        except Exception:
            buttons = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textStartsWith("Cobrar ")')
            if not buttons:
                raise AssertionError("No se encuentra el botón de cobro")
            button = buttons[0]
        button_text = button.text.strip()
        if not button_text.startswith("Cobrar "):
            raise AssertionError(f"Texto inesperado en el botón de cobro: {button_text!r}")
        amount = button_text.replace("Cobrar ", "", 1).strip()
        date = datetime.now().strftime("%d/%m/%Y, %H:%M")
        save_ticket_history(date, amount)
        print(f"Ticket guardado: fecha={date!r}, importe={amount!r}")

    def click_pay(self):
        self.click(self.ENVIAR_A_COCINA)
        self.save_ticket_data()
        self.click(self.COBRAR_40)

    def click_verify_pay(self):
        self.save_ticket_data()
        self.click(self.COBRAR_40)
