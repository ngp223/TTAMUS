from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
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

    def access_products(self):
        self.scroll_text("Productos")
        self.click(self.PRODUCTS)

    def create_product(self):
        self.created_product = f"Producto QA{datetime.now():%d%m%H%M}"
        self.click(self.NEW_PRODUCT)
        self.write(self.PRODUCT_NAME, self.created_product)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.PRODUCT_NAME)

    def check_product_created(self):
        self.write(self.PRODUCTS_SEARCH, self.created_product)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_product}")')
        self.wait_visibility(locator)

    def modify_product(self):
        self.write(self.PRODUCTS_SEARCH, self.created_product)
        self.click(self.EDIT)
        self.created_product += f"_modificado_{datetime.now():%H%M%S}"
        self.write(self.PRODUCT_NAME, self.created_product)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.PRODUCT_NAME)
        self.modified_product = self.created_product

    def check_product_modified(self):
        self.write(self.PRODUCTS_SEARCH, self.modified_product)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_product}")')
        self.wait_visibility(locator)

    def delete_product(self):
        self.write(self.PRODUCTS_SEARCH, self.modified_product)
        self.driver.hide_keyboard()
        self.wait_clickable(self.DELETE).click()
        self.click(self.CONFIRM_DELETE)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_product}")')
        self.wait_invisibility(locator)