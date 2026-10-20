from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage


class BackupsPage(BasePage):
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    COPIAS_SEGURIDAD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copias de Seguridad").instance(0)')
    DESCARGAR_COPIA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Descargar copia cifrada")')
    COPIA_LISTA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copia lista")')

    def __init__(self, driver):
        super().__init__(driver)

    def access_backup(self):
        self.scroll_hasta_texto("Copias de Seguridad")
        self.click(self.COPIAS_SEGURIDAD)

    def download_backup(self):
        self.escribir(self.PASSWORD, TEST_PASSWORD)
        self.click(self.DESCARGAR_COPIA)

    def verify_backup(self):
        return self.existe(self.COPIA_LISTA, timeout=15)
