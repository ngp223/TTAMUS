from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class CategoriesPage(BasePage):
    ADD_CATEGORY = BasePage.by_text("Añadir Categoría")
    CATEGORY_NAME = BasePage.by_id("category-edit-name")
    CATEGORY_ORDER = BasePage.by_id("category-edit-order")
    CREATE_SAVE = BasePage.by_id("category-edit-save")
    EDIT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*button-tam-btn-1")')
    DELETE_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches("categories-delete-.*")')
    SEARCH_CATEGORIES = BasePage.by_id("categories-search")

    def __init__(self, driver):
        super().__init__(driver)
        self.created_category = None

    def access_categories(self):
        self.open_menu("Categorías")

    def create_category(self):
        self.created_category = f"Categoria QA{datetime.now():%d%m%H%M%S}"
        self.click(self.ADD_CATEGORY)
        self.write(self.CATEGORY_NAME, self.created_category)
        self.click(self.CATEGORY_ORDER)
        self.wait_visibility(self.CATEGORY_ORDER).clear()
        self.value_write(self.CATEGORY_ORDER, "0")
        self.click_and_wait_gone(self.CREATE_SAVE, self.CATEGORY_NAME)

    def check_category_created(self):
        self.search_and_find(self.SEARCH_CATEGORIES, self.created_category)

    def modify_category(self):
        self.check_category_created()
        self.click(self.EDIT)
        self.created_category += f"_modificado_{datetime.now():%H%M%S}"
        self.write(self.CATEGORY_NAME, self.created_category)
        self.click_and_wait_gone(self.CREATE_SAVE, self.CATEGORY_NAME)

    def check_category_modified(self):
        self.check_category_created()

    def delete_category(self):
        self.check_category_modified()
        self.confirm_delete(self.DELETE_ICON, self.by_text(self.created_category))