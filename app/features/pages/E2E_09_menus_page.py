
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT
from datetime import datetime


class MenusPage(BasePage):
    MENUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Menús")')
    NEW_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nuevo Menú")')
    MENU_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("menu-edit-name")')
    NEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    ADD_PRODUCT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-sections-1-section-section-{section}-div-section__body-1-button-link-1")')
    SAVE_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("menu-edit-save")')
    EDIT = "contains(@resource-id,'-span-col-1-button-tam-btn-2')"
    TRASH = "starts-with(@resource-id,'menus-delete-')"
    DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_menu = None
        self.modified_description = None

    def select_product(self, section, product):
        self.driver.switch_to.context("NATIVE_APP")
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass
        self.click((self.ADD_PRODUCT[0], self.ADD_PRODUCT[1].format(section=section)))
        try:
            self.driver.switch_to.context("WEBVIEW_com.tamus.pos")
            locator = (AppiumBy.XPATH, f'//*[contains(@id,"section-section-{section}-") and contains(@id,"button-picker__item-") and normalize-space(.)="{product}"]')
            self.click(locator)
        finally:
            self.driver.switch_to.context("NATIVE_APP")

    def open_menus(self):
        self.driver.switch_to.context("NATIVE_APP")
        self.click(self.MENUS)

    def create_menu(self):
        self.created_menu = f"Menu diario QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.click(self.NEW_MENU)
        self.write(self.MENU_NAME, self.created_menu)
        self.click(self.NEXT)
        self.select_product(1, "Tortilla de patata")
        self.select_product(2, "Pulpo a la brasa")
        self.select_product(3, "Tarta de queso")
        self.click(self.SAVE_MENU)
        self.find_menu()

    def find_menu(self):
        if not self.created_menu:
            raise Exception("No existe menu")
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_menu}")')
        return self.wait_visibility(locator, WAIT_TIMEOUT)

    def find_menu_action(self, action):
        self.find_menu()
        locator = (AppiumBy.XPATH, f'//*[@text="{self.created_menu}"]/ancestor::*[.//*[@resource-id and {action}]][1]//*[@resource-id and {action}]')
        return self.wait_visibility(locator, WAIT_TIMEOUT)

    def modify_menu(self):
        self.find_menu_action(self.EDIT).click()
        self.modified_description = f"Menu diario QA {datetime.now().strftime('%Y%m%d_%H%M%S')} modificado"
        self.write(self.MENU_NAME, self.modified_description)
        self.click(self.NEXT)
        self.click(self.SAVE_MENU)
        self.created_menu = self.modified_description

    def verify_modified_menu(self):
        self.created_menu = self.modified_description
        self.find_menu()

    def delete_menu(self):
        self.find_menu_action(self.TRASH).click()
        self.click(self.DELETE)
