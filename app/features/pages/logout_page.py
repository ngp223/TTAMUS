from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from features.config.test_config import INITIAL_USER, WEBVIEW_CONTEXT


class LogoutPage(BasePage):
    USER_NATIVE = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{INITIAL_USER}")')
    USER_MENU = (AppiumBy.XPATH, f'//*[normalize-space(.)="{INITIAL_USER}"]')
    EXIT_POS_MODE = (AppiumBy.XPATH, '//*[normalize-space(.)="Salir"]')
    ACTIVE_TERMINAL = (AppiumBy.XPATH, '//*[normalize-space(.)="Activar terminal"]')

    def find_user(self):
        for context_name, locator in (("NATIVE_APP", self.USER_NATIVE), (WEBVIEW_CONTEXT, self.USER_MENU)):
            try:
                self.driver.switch_to.context(context_name)
                for element in self.driver.find_elements(*locator):
                    if element.is_displayed() and element.is_enabled():
                        return element
            except Exception:
                continue
        self.driver.switch_to.context("NATIVE_APP")
        return None

    def logout(self):
        WebDriverWait(self.driver, 10).until(lambda driver: self.find_user()).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.EXIT_POS_MODE)).click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.ACTIVE_TERMINAL))
        self.driver.switch_to.context("NATIVE_APP")