from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils

class ReportsPage(BasePage):
    REPORTS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Informes")')
    CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías Distribución de ventas por familia de productos. Abrir informe")')
    TITLE_CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías")')
    DISTRIBUTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Distribución")')
    CARNES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" Carnes")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile = MobileUtils(driver)

    def open_reports(self):
        self.click(self.REPORTS)

    def open_categories_report(self):
        self.click(self.CATEGORIES)

    def verify_categories_report(self):
        self.wait_visibility(self.TITLE_CATEGORIES, timeout=15)
        self.wait_visibility(self.DISTRIBUTION, timeout=15)
        self.wait_visibility(self.CARNES, timeout=15)
