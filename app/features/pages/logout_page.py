
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from features.pages.base_page import BasePage
from features.config.test_config import INITIAL_USER

class LogoutPage(BasePage):
    USER_MENU = (AppiumBy.XPATH, f'//*[normalize-space(.)="{INITIAL_USER}"]')
    EXIT_POS_MODE = (AppiumBy.XPATH, '//*[normalize-space(.)="Salir"]')
    ACTIVE_TERMINAL = (AppiumBy.XPATH, '//*[normalize-space(.)="Activar terminal"]')

    def find_user(self):
        webview = next((c for c in self.driver.contexts if "WEBVIEW" in c.upper()), None)
        if not webview:
            return None
        self.driver.switch_to.context(webview)
        for element in self.driver.find_elements(*self.USER_MENU):
            if element.is_displayed() and element.is_enabled():
                return element
        return None

    def logout(self):
        elemento = WebDriverWait(self.driver, 10).until(lambda driver: self.find_user())
        elemento.click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EXIT_POS_MODE)).click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.ACTIVE_TERMINAL))
        self.driver.switch_to.context("NATIVE_APP")

    def logout_if_exists(self):
        try:
            elemento = WebDriverWait(self.driver, 3).until(lambda driver: self.find_user())
        except TimeoutException:
            self.driver.switch_to.context("NATIVE_APP")
            return False
        if elemento is None:
            self.driver.switch_to.context("NATIVE_APP")
            return False
        try:
            elemento.click()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EXIT_POS_MODE)).click()
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.ACTIVE_TERMINAL))
            return True
        finally:
            self.driver.switch_to.context("NATIVE_APP")
