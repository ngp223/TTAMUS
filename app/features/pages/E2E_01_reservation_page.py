from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class ReservationPage(BasePage):
    VISTA_MESAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Vista de mesas")')

    def __init__(self, driver):
        super().__init__(driver)

    def comprobar_vista_mesas(self):
        return self.esperar_visible(self.VISTA_MESAS)
