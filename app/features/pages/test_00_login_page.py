from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_EMAIL, TEST_PASSWORD, REST1, REST1_PIN, REST1_USUARIO, REST1_USUARIO_PIN
from features.pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-1")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-2")')
    ACTIVAR_TERMINAL = (AppiumBy.XPATH, '//android.widget.Button[@text="Activar terminal"]')
    REST1 = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{REST1}")')
    ENTRAR_REST1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar a este restaurante")')
    REST1_USUARIO = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{REST1_USUARIO}")')
    ENTRAR_POS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar al POS")')

    def __init__(self, driver):
        super().__init__(driver)

    def login(self):
        self.escribir(self.EMAIL, TEST_EMAIL)
        self.escribir(self.PASSWORD, TEST_PASSWORD)
        self.click(self.ACTIVAR_TERMINAL)
        self.click(self.REST1)

        for digit in REST1_PIN:
            pin_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")')
            self.click(pin_button)

        self.scroll_hasta_texto("Entrar a este restaurante")
        self.click(self.ENTRAR_REST1)
        self.click(self.REST1_USUARIO)

        for digit in REST1_USUARIO_PIN:
            pin_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")')
            self.click(pin_button)

        self.click(self.ENTRAR_POS)
