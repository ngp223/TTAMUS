from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT
from datetime import datetime


class MenusPage(BasePage):
    MENUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Menús")')
    NEW_MENU = (AppiumBy.CSS_SELECTOR, '#menus-add')
    MENU_NAME = (AppiumBy.CSS_SELECTOR, '#menu-edit-name')
    NEXT = (AppiumBy.CSS_SELECTOR, '#menu-edit-next')
    ADD_PRODUCT = (AppiumBy.CSS_SELECTOR, '#cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-sections-1-section-section-{section}-div-section__body-1-button-link-1')
    PRODUCT = (AppiumBy.CSS_SELECTOR, '[id*="button-picker__item-"]')
    SAVE_MENU = (AppiumBy.CSS_SELECTOR, '#menu-edit-save')
    EDIT = (AppiumBy.CSS_SELECTOR, '[id$="-span-col-1-button-tam-btn-2-span-tam-btn__content-1-span-tam-btn__icon-1"]')
    TRASH = (AppiumBy.CSS_SELECTOR, '[id*="menus-delete-"]')
    DELETE = (AppiumBy.CSS_SELECTOR, '#confirm-modal-accept')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_menu = None
        self.modified_description = None

    def select_product(self, section, product):
        add_product = (self.ADD_PRODUCT[0], self.ADD_PRODUCT[1].format(section=section))
        self.click(add_product)
        products = self.driver.find_elements(*self.PRODUCT)
        next(element for element in products if element.text.strip() == product).click()

    def open_menus(self):
        self.driver.switch_to.context("NATIVE_APP")
        self.click(self.MENUS)
        self.driver.switch_to.context("WEBVIEW_com.tamus.pos")

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
        locator = (AppiumBy.XPATH, f'//*[normalize-space(text())="{self.created_menu}"]')
        return self.wait_visibility(locator, WAIT_TIMEOUT)

    def find_menu_action(self, action):
        self.find_menu()
        elementos = self.driver.find_elements(*action)
        return elementos[0]

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