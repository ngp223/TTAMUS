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

    def __init__(self, driver):
        super().__init__(driver)

    def login_in(self, context):
        webview = next((c for c in self.driver.contexts if "WEBVIEW" in c.upper()), None)
        if not webview:
            raise Exception("No se encuentra el contexto WEBVIEW para iniciar sesión")
        self.driver.switch_to.context(webview)
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.EMAIL))
        self.write(self.EMAIL, TEST_EMAIL)
        self.write(self.PASSWORD, TEST_PASSWORD)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ACTIVE_TERMINAL)).click()
        self.driver.switch_to.context("NATIVE_APP")
        self.click(self.REST1)
        for digit in REST1_PIN:
            self.click((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")'))
        self.scroll_text("Entrar a este restaurante")
        self.click(self.OPEN_REST1)
        self.click(self.REST1_USER)
        for digit in REST1_USER_PIN:
            self.click((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")'))
        self.click(self.OPEN_POS)
        self.click(self.EXPAND)
        context.logged_in = True
        print("Login completado")

    def active_terminal(self):
        webview = next((c for c in self.driver.contexts if "WEBVIEW" in c.upper()), None)
        if not webview:
            return False
        contexto_anterior = self.driver.current_context
        try:
            self.driver.switch_to.context(webview)
            return self.exists(self.ACTIVE_TERMINAL, timeout=3)
        finally:
            self.driver.switch_to.context(contexto_anterior)
