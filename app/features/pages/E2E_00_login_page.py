from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_EMAIL, TEST_PASSWORD, POS_PIN
from features.pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-1")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-2")')
    ACTIVAR_TERMINAL = (AppiumBy.XPATH, '//android.widget.Button[@text="Activar terminal"]')
    ENTRAR_POS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar al POS")')

    def __init__(self, driver):
        super().__init__(driver)

    def login(self):
        self.escribir(self.EMAIL, TEST_EMAIL)
        self.escribir(self.PASSWORD, TEST_PASSWORD)
        self.click(self.ACTIVAR_TERMINAL)
        for digit in POS_PIN:
            pin_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")')
            self.click(pin_button)
        self.click(self.ENTRAR_POS)
