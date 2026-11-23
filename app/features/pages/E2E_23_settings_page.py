from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class SettingsPage(BasePage):
    SETTINGS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Ajustes")')
    def access_settings(self):
        self.scroll_text_any("Ajustes")
        self.click(self.SETTINGS)