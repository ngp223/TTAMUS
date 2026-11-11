from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.created_product = f"Producto QA{datetime.now():%d%m%Y%H%M%S}"
        self.click(self.NEW_PRODUCT)
        self.write(self.PRODUCT_NAME, self.created_product)
        self.driver.hide_keyboard()
        self.click(self.CREATE_SAVE)
        WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located(self.PRODUCT_NAME))

    def check_product_created(self):
        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.PRODUCTS_SEARCH))
        search.click()
        search.clear()
        search.send_keys(self.created_product)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_product}")')
        self.wait_visibility(locator)

    def modify_product(self):
        self.write(self.PRODUCTS_SEARCH, self.created_product)
        self.driver.hide_keyboard()
        self.click(self.EDIT)
        self.created_product += f"_modificado_{datetime.now():%d%m%Y%H%M%S}"
        self.write(self.PRODUCT_NAME, self.created_product)
        self.click(self.CREATE_SAVE)
        WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located(self.PRODUCT_NAME))
        self.modified_product = self.created_product

    def check_product_modified(self):
        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.PRODUCTS_SEARCH))
        search.click()
        search.clear()
        search.send_keys(self.modified_product)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_product}")')
        self.wait_visibility(locator)

    def delete_product(self):
        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.PRODUCTS_SEARCH))
        search.click()
        search.clear()
        search.send_keys(self.created_product)
        self.driver.hide_keyboard()
        self.click(self.DELETE)
        self.click(self.CONFIRM_DELETE)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_product}")')
        WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located(locator))
