from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils

class ReportsPage(BasePage):
    REPORTS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Informes")')
    CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías Distribución de ventas por familia de productos. Abrir informe")')
    TITLE_CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías")')
    CONCENTRATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CONCENTRACIÓN")')
    COFFEES_INFUSIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" Cafés e infusiones")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile = MobileUtils(driver)

    def open_reports(self):
        self.click(self.REPORTS)

    def open_categories_report(self):
        self.click(self.CATEGORIES)

    def verify_categories_report(self):
        self.wait_visibility(self.TITLE_CATEGORIES, timeout=15)
        print("Título encontrado: Categorías")
        self.wait_visibility(self.CONCENTRATION, timeout=15)
        print("Apartado encontrado: CONCENTRACIÓN")
        self.mobile.swipe_up()
        self.mobile.swipe_up()
        self.wait_visibility(self.COFFEES_INFUSIONS, timeout=15)
        print("Categoría encontrada: Cafés e infusiones")