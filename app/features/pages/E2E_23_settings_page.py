from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class SettingsPage(BasePage):
    SETTINGS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Ajustes")')
    GENERAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("General")')
    APPEARANCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Apariencia")')
    ACCESSIBILITY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Accesibilidad")')
    NOTIFICATIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Notificaciones")')
    TAXES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Impuestos")')
    BUSINESS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Negocio")')
    ACCOUNT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cuenta")')

    def access_settings(self):
        self.click(self.SETTINGS)

    def general(self):
        self.click(self.GENERAL)

    def appearance(self):
        self.click(self.APPEARANCE)

    def accessibility(self):
        self.click(self.ACCESSIBILITY)

    def notifications(self):
        self.click(self.NOTIFICATIONS)

    def taxes(self):
        self.click(self.TAXES)

    def business(self):
        self.click(self.BUSINESS)

    def account(self):
        self.click(self.ACCOUNT)