
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage


class CategoriesPage(BasePage):
    CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Categorías")')
    ADD_CATEGORY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Añadir Categoría")')
    CATEGORY_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("category-edit-name")')
    CATEGORY_ORDER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("category-edit-order")')
    CREATE_SAVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("category-edit-save")')
    EDIT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*button-tam-btn-1")')
    DELETE_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches("categories-delete-.*")')
    CONFIRM_DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')
    SEARCH_CATEGORIES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("categories-search")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_category = None

    def access_categories(self):
        self.scroll_text("Categorías")
        self.click(self.CATEGORIES)

    def create_category(self):
        self.created_category = f"Categoria QA{datetime.now():%d%m%H%M%S}"
        self.click(self.ADD_CATEGORY)
        self.write(self.CATEGORY_NAME, self.created_category)
        self.click(self.CATEGORY_ORDER)
        order = self.driver.find_element(*self.CATEGORY_ORDER)
        order.clear()
        self.value_write(self.CATEGORY_ORDER, "0")
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.CATEGORY_NAME)

    def check_category_created(self):
        self.write(self.SEARCH_CATEGORIES, self.created_category)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_category}")')
        self.wait_visibility(locator)

    def modify_category(self):
        self.write(self.SEARCH_CATEGORIES, self.created_category)
        self.driver.hide_keyboard()
        self.click(self.EDIT)
        self.created_category += f"_modificado_{datetime.now():%H%M%S}"
        self.write(self.CATEGORY_NAME, self.created_category)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.CATEGORY_NAME)

    def check_category_modified(self):
        self.write(self.SEARCH_CATEGORIES, self.created_category)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_category}")')
        self.wait_visibility(locator)

    def delete_category(self):
        self.write(self.SEARCH_CATEGORIES, self.created_category)
        self.driver.hide_keyboard()
        self.click(self.DELETE_ICON)
        self.click(self.CONFIRM_DELETE)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_category}")')
        self.wait_invisibility(locator)
