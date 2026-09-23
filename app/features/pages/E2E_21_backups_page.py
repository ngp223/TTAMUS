from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage

class BackupsPage(BasePage):
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    COPIAS_SEGURIDAD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copias de Seguridad").instance(0)')
    DESCARGAR_COPIA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Descargar copia cifrada")')
    COPIA_LISTA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copia lista")')

    def acceder_copias_seguridad(self):
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Copias de Seguridad"))')
        self.click(self.COPIAS_SEGURIDAD)

    def descargar_backup(self):
        self.escribir(self.PASSWORD, TEST_PASSWORD)
        self.click(self.DESCARGAR_COPIA)

    def comprobar_copia_lista(self):
        return self.existe(self.COPIA_LISTA, timeout=15)
