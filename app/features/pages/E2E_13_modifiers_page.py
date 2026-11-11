
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage


class ModifiersPage(BasePage):
    MODIFIERS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Modificadores")')
    NEW_GROUP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nuevo Grupo")')
    MODIFIER_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("modifier-group-name")')
    SAVE_GROUP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("modifier-group-save")')
    MODIFIERS_SEARCH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("modifiers-search")')
    EDIT = (AppiumBy.ACCESSIBILITY_ID, "Editar")
    DELETE = (AppiumBy.ACCESSIBILITY_ID, "Eliminar")
    CONFIRM_DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_modifier = None
        self.modified_modifier = None

    def access_modifiers(self):
        self.scroll_text("Modificadores")
        self.click(self.MODIFIERS)

    def create_modifier(self):
        self.created_modifier = f"ModificadorQA{datetime.now():%d%m%Y%H%M%S}"
        self.click(self.NEW_GROUP)
        self.write(self.MODIFIER_NAME, self.created_modifier)
        self.driver.hide_keyboard()
        self.click(self.SAVE_GROUP)
        self.wait_invisibility(self.MODIFIER_NAME)

    def check_modifier_created(self):
        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.MODIFIERS_SEARCH))
        search.click()
        search.clear()
        search.send_keys(self.created_modifier)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_modifier}")')
        self.wait_visibility(locator)

    def modify_modifier(self):
        self.write(self.MODIFIERS_SEARCH, self.created_modifier)
        self.driver.hide_keyboard()
        self.click(self.EDIT)
        self.created_modifier += f"_modificado_{datetime.now():%d%m%Y%H%M%S}"
        self.write(self.MODIFIER_NAME, self.created_modifier)
        self.click(self.SAVE_GROUP)
        self.wait_invisibility(self.MODIFIER_NAME)
        self.modified_modifier = self.created_modifier

    def check_modifier_modified(self):
        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.MODIFIERS_SEARCH))
        search.click()
        search.clear()
        search.send_keys(self.modified_modifier)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_modifier}")')
        self.wait_visibility(locator)

    def delete_modifier(self):
        search = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.MODIFIERS_SEARCH))
        search.click()
        search.clear()
        search.send_keys(self.modified_modifier)
        self.driver.hide_keyboard()
        self.click(self.DELETE)
        self.click(self.CONFIRM_DELETE)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_modifier}")')
        self.wait_invisibility(locator)
