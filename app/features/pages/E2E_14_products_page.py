from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from features.pages.base_page import BasePage


class ProductsPage(BasePage):
    NEW_PRODUCT = BasePage.by_text("Nuevo Producto")
    PRODUCT_NAME = BasePage.by_id("product-edit-name")
    PRODUCTS_SEARCH = BasePage.by_id("products-search")
    CREATE_SAVE = BasePage.by_id("product-edit-save")

    def __init__(self, driver):
        super().__init__(driver)
        self.created_product = None
        self.modified_product = None

    def _row_locator(self, name):
        return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}").className("android.widget.TextView")')

    def _write_clean(self, locator, text):
        el = self.wait_visibility(locator)
        el.click()
        el.clear()
        if el.text.strip():
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.BACK_SPACE)
        el.send_keys(text)
        current = el.text.strip()
        if current != text:
            raise AssertionError(f"Error escribiendo '{text}' (actual: '{current}')")

    def _find_row(self, name):
        if self.exists(self._row_locator(name), timeout=1):
            return
        self._write_clean(self.PRODUCTS_SEARCH, name)
        try:
            return self.wait_visibility(self._row_locator(name), timeout=10)
        except TimeoutException:
            raise AssertionError(f"No aparece en listado: '{name}'")

    def access_products(self):
        self.open_menu("Productos")

    def create_product(self):
        self.created_product = f"Producto QA{datetime.now():%d%m_%H%M%S}"
        self.click(self.NEW_PRODUCT)
        self._write_clean(self.PRODUCT_NAME, self.created_product)
        self.click_and_wait_gone(self.CREATE_SAVE, self.PRODUCT_NAME)
        self.wait_visibility(self.PRODUCTS_SEARCH, timeout=10)

    def check_product_created(self):
        self._find_row(self.created_product)

    def modify_product(self):
        self._find_row(self.created_product)
        self.click(self.EDIT)
        self.created_product += f"_modificado_{datetime.now():%H%M%S}"
        self._write_clean(self.PRODUCT_NAME, self.created_product)
        self.click_and_wait_gone(self.CREATE_SAVE, self.PRODUCT_NAME)
        self.modified_product = self.created_product
        self.wait_visibility(self.PRODUCTS_SEARCH, timeout=10)

    def check_product_modified(self):
        self._find_row(self.modified_product)

    def delete_product(self):
        target = self.modified_product or self.created_product
        self._find_row(target)
        self.click(self.DELETE)
        self.click(self.CONFIRM_DELETE)
        self.wait_invisibility(self.CONFIRM_DELETE, timeout=10)
        self._write_clean(self.PRODUCTS_SEARCH, target)
        try:
            self.wait_invisibility(self._row_locator(target), timeout=10)
        except TimeoutException:
            raise AssertionError(f"Sigue apareciendo tras borrar: '{target}'")