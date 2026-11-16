from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.config.test_config import TEST_EMAIL, TEST_PASSWORD, REST1, REST1_PIN, REST1_USER, REST1_USER_PIN
from features.pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL = (AppiumBy.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD = (AppiumBy.CSS_SELECTOR, 'input[type="password"]')
    ACTIVE_TERMINAL = (AppiumBy.XPATH, '//button[contains(normalize-space(.), "Activar terminal")]')
    REST1 = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{REST1}")')
    OPEN_REST1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar a este restaurante")')
    REST1_USER = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{REST1_USER}")')
    OPEN_POS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar al POS")')
    EXPAND = (AppiumBy.ACCESSIBILITY_ID, "Expandir menú")

    def _enter_pin(self, pin):
        for digit in pin:
            self.click((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")'))

    def login_in(self):
        self.wait_visibility_contexts(self.EMAIL)
        self.write(self.EMAIL, TEST_EMAIL)
        self.write(self.PASSWORD, TEST_PASSWORD)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ACTIVE_TERMINAL)).click()
        self.driver.switch_to.context("NATIVE_APP")
        self.click(self.REST1)
        self._enter_pin(REST1_PIN)
        self.scroll_text("Entrar a este restaurante")
        self.click(self.OPEN_REST1)
        self.click(self.REST1_USER)
        self._enter_pin(REST1_USER_PIN)
        self.click(self.OPEN_POS)
        self.click(self.EXPAND)
        print("Login completado")