from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from features.pages.base_page import BasePage


class ProductsPage(BasePage):
    PRODUCTS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Productos")')
    NEW_PRODUCT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nuevo Producto")')
    PRODUCT_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("product-edit-name")')
    PRODUCTS_SEARCH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("products-search")')
    CREATE_SAVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("product-edit-save")')
    EDIT = (AppiumBy.ACCESSIBILITY_ID, "Editar")
    DELETE = (AppiumBy.ACCESSIBILITY_ID, "Eliminar")
    CONFIRM_DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_product = None
        self.modified_product = None

    def _row_locator(self, name):
        return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}").className("android.widget.TextView")')

    def _get_text(self, el):
        return (el.get_attribute("text") or el.text or "").strip()

    def _write_clean(self, locator, text):
        el = self.wait_visibility(locator, timeout=15)
        el.click()
        el.clear()
        if self._get_text(el):
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.BACK_SPACE)
        el.send_keys(text)
        current = self._get_text(el)
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
        if not self.exists(self.PRODUCTS, timeout=2):
            self.scroll_text("Productos")
        self.click(self.PRODUCTS)
        self.wait_visibility(self.NEW_PRODUCT, timeout=15)

    def create_product(self):
        self.created_product = f"Producto QA{datetime.now():%d%m_%H%M%S}"
        self.click(self.NEW_PRODUCT)
        self._write_clean(self.PRODUCT_NAME, self.created_product)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.PRODUCT_NAME, timeout=15)
        self.wait_visibility(self.PRODUCTS_SEARCH, timeout=10)

    def check_product_created(self):
        self._find_row(self.created_product)

    def modify_product(self):
        self._find_row(self.created_product)
        self.click(self.EDIT)
        self.created_product += f"_modificado_{datetime.now():%H%M%S}"
        self._write_clean(self.PRODUCT_NAME, self.created_product)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.PRODUCT_NAME, timeout=15)
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
        if self.exists(self._row_locator(target), timeout=2):
            raise AssertionError(f"Sigue existiendo tras borrar: '{target}'")