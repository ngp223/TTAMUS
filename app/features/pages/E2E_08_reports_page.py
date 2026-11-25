from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils


class ReportsPage(BasePage):
    REPORTS = BasePage.by_text("Informes")
    CATEGORIES = BasePage.by_text("Categorías Distribución de ventas por familia de productos. Abrir informe")
    TITLE_CATEGORIES = BasePage.by_text("Categorías")
    DISTRIBUTION = BasePage.by_text("Distribución")
    CARNES = BasePage.by_text(" Carnes")

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile = MobileUtils(driver)

    def open_reports(self):
        self.click(self.REPORTS)

    def open_categories_report(self):
        self.click(self.CATEGORIES)

    def verify_categories_report(self):
        self.wait_visibility(self.TITLE_CATEGORIES)
        self.wait_visibility(self.DISTRIBUTION)
        self.mobile.swipe_up()
        self.wait_visibility(self.CARNES)