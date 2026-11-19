from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class ConfigurationGuidePage(BasePage):
    GUIDE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Guía de configuración")')
    GUIDE_OPEN_WIZARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("guide-open-wizard")')
    GUIDE_WIZARD_SKIP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("guide-wizard-skip")')
    GUIDE_WIZARD_START_SELLING = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("guide-wizard-start-selling")')
    GUIDE_WIZARD_OPEN_CERTIFICATE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("guide-wizard-open-certificate")')

    def access_configurationguide(self):
        self.scroll_text("Guía de configuración")
        self.click(self.GUIDE)

    def configure(self):
        self.click(self.GUIDE_OPEN_WIZARD)
        if not self.exists(self.GUIDE_WIZARD_SKIP):
            self.click(self.GUIDE_WIZARD_OPEN_CERTIFICATE)
        self.click(self.GUIDE_WIZARD_SKIP)
        self.click(self.GUIDE_WIZARD_START_SELLING)
