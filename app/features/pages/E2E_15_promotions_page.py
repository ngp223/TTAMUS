from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class PromotionsPage(BasePage):
    PROMOTIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Promociones")')
    NEW_PROMOTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva Promoción")')
    PROMOTION_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("promotion-edit-name")')
    NEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("promotion-edit-next")')
    PROMOTIONS_SEARCH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("promotions-search")')
    CREATE_SAVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("promotion-edit-save")')
    EDIT = (AppiumBy.ACCESSIBILITY_ID, "Editar")
    DELETE = (AppiumBy.ACCESSIBILITY_ID, "Eliminar")
    CONFIRM_DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_promotion = None
        self.modified_promotion = None

    def access_promotions(self):
        self.scroll_text("Promociones")
        self.click(self.PROMOTIONS)

    def create_promotion(self):
        self.created_promotion = f"Promoción QA{datetime.now():%d%m%H%M}"
        self.click(self.NEW_PROMOTION)
        self.write(self.PROMOTION_NAME, self.created_promotion)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.PROMOTION_NAME)

    def check_promotion_created(self):
        self.search_and_find(self.PROMOTIONS_SEARCH, self.created_promotion)

    def modify_promotion(self):
        self.check_promotion_created()
        self.click(self.EDIT)
        self.created_promotion += f"_modificado_{datetime.now():%d%m%H%M}"
        self.write(self.PROMOTION_NAME, self.created_promotion)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.PROMOTION_NAME)
        self.modified_promotion = self.created_promotion

    def check_promotion_modified(self):
        self.search_and_find(self.PROMOTIONS_SEARCH, self.modified_promotion)

    def delete_promotion(self):
        self.check_promotion_modified()
        self.click(self.DELETE)
        self.click(self.CONFIRM_DELETE)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_promotion}")')
        self.wait_invisibility(locator)