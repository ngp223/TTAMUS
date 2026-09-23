from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class LogoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def logout(self, user_initial):
        inicial = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{user_initial}")')
        salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')
        self.click(inicial)
        self.click(salir)
