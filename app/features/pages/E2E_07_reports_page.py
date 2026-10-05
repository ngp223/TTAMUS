from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils

class ReportsPage(BasePage):
    INFORMES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Informes")')
    CATEGORIAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías Distribución de ventas por familia de productos. Abrir informe")')
    TITULO_CATEGORIAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías")')
    CONCENTRACION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CONCENTRACIÓN")')
    CAFES_INFUSIONES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" Cafés e infusiones")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile = MobileUtils(driver)

    def open_reports(self):
        self.click(self.INFORMES)

    def open_categories_report(self):
        self.click(self.CATEGORIAS)

    def verify_categories_report(self):
        self.esperar_visible(self.TITULO_CATEGORIAS, timeout=15)
        print("Título encontrado: Categorías")
        self.esperar_visible(self.CONCENTRACION, timeout=15)
        print("Apartado encontrado: CONCENTRACIÓN")
        self.mobile.swipe_up()
        self.mobile.swipe_up()
        self.esperar_visible(self.CAFES_INFUSIONES, timeout=15)
        print("Categoría encontrada: Cafés e infusiones")