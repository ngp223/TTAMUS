from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from datetime import datetime

class BillingPage(BasePage):
    FACTURACION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Facturación")')
    NUEVA_FACTURA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva Factura")')
    CONCEPTO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-10")')
    CANTIDAD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-11")')
    PRECIO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-12")')
    CLIENTE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1")')
    CLIENTE_OPCION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1-opt-1")')
    CONFIRMAR_EMITIR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirmar y Emitir Factura")')
    CONCEPTO_VALOR = "ProductoQA"
    CANTIDAD_VALOR = "2"
    PRECIO_VALOR = "20"

    def __init__(self, driver):
        super().__init__(driver)

    def esperar_popup_fuera(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Reintentar")')))
        except:
            pass

    def open_billing(self):
        self.esperar_popup_fuera()
        self.click(self.FACTURACION)
        self.esperar_popup_fuera()

    def create_new_invoice(self):
        self.click(self.NUEVA_FACTURA)
        self.click(self.CLIENTE)
        self.click(self.CLIENTE_OPCION)
        self.escribir(self.CONCEPTO, self.CONCEPTO_VALOR)
        self.escribir_valor(self.CANTIDAD, self.CANTIDAD_VALOR)
        self.escribir_valor(self.PRECIO, self.PRECIO_VALOR)
        self.driver.hide_keyboard()
        ahora = datetime.now()
        self.fecha_factura = f"{ahora.day}/{ahora.month}/{ahora.year}, {ahora.strftime('%H:%M')}"
        self.click(self.CONFIRMAR_EMITIR)

    def invoice_created_successfully(self):
        assert not self.existe(self.CONFIRMAR_EMITIR, timeout=2), "La factura no se ha creado correctamente"

    def invoice_appears_in_list(self):
        locator = (AppiumBy.XPATH, f'//android.widget.TextView[contains(@text, "{self.fecha_factura}")]')
        elemento = self.esperar_visible(locator, timeout=5)
        print(f"FACTURA ENCONTRADA: {elemento.text}", flush=True)