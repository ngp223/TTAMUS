from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class ReservationPage(BasePage):
    VISTA_MESAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Vista de mesas")')
    SALON_PRINCIPAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salón principal")')
    MESA_SAL_03 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAL-04")')
    COMENSALES_3 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("3")')
    ACEPTAR =(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Aceptar")')
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
    MESA_LIBERADA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Mesa liberada")')

    def __init__(self, driver):
        super().__init__(driver)

    def comprobar_vista_mesas(self):
        return self.esperar_visible(self.VISTA_MESAS)

    def select_table(self):
        self.click(self.SALON_PRINCIPAL)
        self.click(self.MESA_SAL_03)

    def select_guests(self):
        self.click(self.COMENSALES_3)

    def click_accept_guests(self):
        self.click(self.ACEPTAR)

    def select_product_arroz_bogavante(self):
        self.click(self.CARNES)
        self.click(self.SOLOMILLO_FOIE)
        self.click(self.VERDURAS_PLANCHA)
        self.click(self.POCO_HECHO)
        self.click(self.AÑADIR)
        self.click(self.ARROCES)
        self.click(self.RISOTTO_SETAS)

    def increase_product(self):
        self.click(self.AUMENTAR_PRODUCTO)

    def click_realizar_pago(self):
        self.click(self.ENVIAR_A_COCINA)
        self.click(self.COBRAR_40)

    def click_confirmar_pago(self):
        self.click(self.COBRAR_40)

