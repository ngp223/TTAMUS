import random
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT, WEBVIEW_CONTEXT


class MenusPage(BasePage):
    MENUS = BasePage.by_text("Menús")
    NEW_MENU = (AppiumBy.CSS_SELECTOR, '#menus-add')
    MENU_NAME = (AppiumBy.CSS_SELECTOR, '#menu-edit-name')
    NEXT = (AppiumBy.CSS_SELECTOR, '#menu-edit-next')
    PRODUCT = (AppiumBy.CSS_SELECTOR, '[id*="button-picker__item-"]')
    SAVE_MENU = (AppiumBy.CSS_SELECTOR, '#menu-edit-save')
    EDIT = (AppiumBy.CSS_SELECTOR, '[id$="-span-col-1-button-tam-btn-2-span-tam-btn__content-1-span-tam-btn__icon-1"]')
    TRASH = (AppiumBy.CSS_SELECTOR, '[id*="menus-delete-"]')
    DELETE = (AppiumBy.CSS_SELECTOR, '#confirm-modal-accept')
    ADD_PRODUCT = (AppiumBy.CSS_SELECTOR, '[id^="cdk-dialog-"][id*="-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-sections-1-section-section-{section}-div-section__body-1-button-link-1"]')
    MENU_NAME_XPATH = '//*[normalize-space(text())="{}"]'
    ICONS = ("add", "check", "check_circle")

    def __init__(self, driver):
        super().__init__(driver)
        self.created_menu = None
        self.modified_description = None

    def _pick_product(self, locator, selected_products):
        items = []
        for p in self.driver.find_elements(*locator):
            lines = [l for l in p.text.strip().splitlines() if l.strip() and l.strip() not in self.ICONS]
            if lines and lines[0].strip() not in selected_products:
                items.append((p, lines[0].strip()))
        if not items:
            return False
        product, name = random.choice(items)
        product.click()
        return name

    def select_product(self, section, selected_products):
        add_product = (self.ADD_PRODUCT[0], self.ADD_PRODUCT[1].format(section=section))
        self.click(add_product, timeout=45)
        locator = (AppiumBy.CSS_SELECTOR, f'[id*="section-section-{section}-"][id*="button-picker__item-"]')
        name = WebDriverWait(self.driver, 15, ignored_exceptions=(StaleElementReferenceException,)).until(lambda d: self._pick_product(locator, selected_products))
        selected_products.append(name)
        print(f"Producto seleccionado en sección {section}: {name}")

    def open_menus(self):
        self.driver.switch_to.context("NATIVE_APP")
        self.click(self.MENUS)
        self.driver.switch_to.context(WEBVIEW_CONTEXT)

    def create_menu(self):
        self.created_menu = f"Menu diario QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.click(self.NEW_MENU)
        self.write(self.MENU_NAME, self.created_menu)
        self.click(self.NEXT)
        selected_products = []
        for section in (1, 2, 3):
            self.select_product(section, selected_products)
        self.click(self.SAVE_MENU)
        self.find_menu()

    def find_menu(self):
        if not self.created_menu:
            raise Exception("No existe menu")
        return self.wait_visibility((AppiumBy.XPATH, self.MENU_NAME_XPATH.format(self.created_menu)), WAIT_TIMEOUT)

    def find_menu_action(self, action):
        row = self.find_menu().find_element(AppiumBy.XPATH, './ancestor::*[starts-with(@id,"cdk-drop-list-") and contains(@id,"div-cdk-drag-")][last()]')
        return row.find_element(*action)

    def modify_menu(self):
        self.find_menu_action(self.EDIT).click()
        self.modified_description = f"Menu diario QA {datetime.now().strftime('%Y%m%d_%H%M%S')} modificado"
        self.write(self.MENU_NAME, self.modified_description)
        self.click(self.NEXT)
        self.click(self.SAVE_MENU)
        self.created_menu = self.modified_description

    def verify_modified_menu(self):
        self.find_menu()

    def delete_menu(self):
        self.find_menu_action(self.TRASH).click()
        self.click(self.DELETE)
        self.wait_invisibility((AppiumBy.XPATH, self.MENU_NAME_XPATH.format(self.created_menu)))