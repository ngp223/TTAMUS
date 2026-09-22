from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.config.test_config import TEST_EMAIL, TEST_PASSWORD, POS_PIN
import time

class LoginPage:
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-1")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-2")')
    ACTIVAR_TERMINAL = (AppiumBy.XPATH,'//android.widget.Button[@text="Activar terminal"]')
    ENTRAR_POS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar al POS")')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self):
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL))
        email_input.clear()
        email_input.send_keys(TEST_EMAIL)
        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD))
        password_input.clear()
        password_input.send_keys(TEST_PASSWORD)
        self.wait.until(EC.element_to_be_clickable(self.ACTIVAR_TERMINAL)).click()
        time.sleep(2)
        for digit in POS_PIN:
            pin_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{digit}")')
            self.wait.until(EC.element_to_be_clickable(pin_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.ENTRAR_POS)).click()

