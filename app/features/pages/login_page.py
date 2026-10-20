
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.config.test_config import TEST_EMAIL, TEST_PASSWORD, REST1, REST1_PIN, REST1_USER, REST1_USER_PIN
from features.pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-1")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-2")')
    ACTIVE_TERMINAL = (AppiumBy.XPATH, '//android.widget.Button[@text="Activar terminal"]')
    REST1 = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{REST1}")')
    OPEN_REST1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar a este restaurante")')
    REST1_USER = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{REST1_USER}")')
    OPEN_POS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar al POS")')

    def __init__(self, driver):
        super().__init__(driver)

    def login_in(self):
        self.write(self.EMAIL, TEST_EMAIL)
        self.write(self.PASSWORD, TEST_PASSWORD)
        self.driver.hide_keyboard()
        if self.exists(self.ACTIVE_TERMINAL, timeout=3):
            self.click(self.ACTIVE_TERMINAL)
        self.click(self.REST1)
        for digit in REST1_PIN:
            pin_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")')
            self.click(pin_button)
        self.scroll_text("Entrar a este restaurante")
        self.click(self.OPEN_REST1)
        self.click(self.REST1_USER)
        for digit in REST1_USER_PIN:
            pin_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")')
            self.click(pin_button)
        self.click(self.OPEN_POS)
        print("Login completado")

    def active_terminal(self):
        return self.exists(self.ACTIVE_TERMINAL)
