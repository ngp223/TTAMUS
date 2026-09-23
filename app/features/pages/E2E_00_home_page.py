from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.menu_usuario = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("A")')
        self.salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')

    def logout(self):
        self.click(self.menu_usuario)
        self.click(self.salir)
