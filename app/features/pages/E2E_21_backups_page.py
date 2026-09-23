from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage

class BackupsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.password = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
        self.copias_seguridad = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copias de Seguridad").instance(0)')
        self.descargar_copia = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Descargar copia cifrada")')
        self.copia_lista = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copia lista")')

    def acceder_copias_seguridad(self):
        self.scroll_hasta_texto("Copias de Seguridad")
        self.click(self.copias_seguridad)

    def descargar_backup(self):
        self.escribir(self.password, TEST_PASSWORD)
        self.click(self.descargar_copia)

    def comprobar_copia_lista(self):
        return self.existe(self.copia_lista, timeout=15)
