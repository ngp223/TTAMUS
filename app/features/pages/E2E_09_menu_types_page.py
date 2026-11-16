from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from features.config.test_config import (
    WAIT_TIMEOUT, MENU_TYPE_STARTERS, MENU_TYPE_PEPPERS, MENU_TYPE_SALADS, MENU_TYPE_SALAD_CESAR)
from datetime import datetime
import time


class MenuTypesPage(BasePage):
    MENU_TYPES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cartas")')
    ADD_MENU_TYPE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Añadir Carta")')
    NAME_MENU_TYPE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("carta-wizard-name")')
    NEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    STARTERS = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{MENU_TYPE_STARTERS}")')
    PEPPERS = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{MENU_TYPE_PEPPERS}")')
    SALADS = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{MENU_TYPE_SALADS}")')
    SALAD_CESAR = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{MENU_TYPE_SALAD_CESAR}")')
    FINISH_AND_SAVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Finalizar y Guardar")')
    BIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Eliminar")')
    DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')
    PREVIOUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Anterior")')
    CLOSE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cerrar")')
    EDIT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Editar")')
    SEE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Ver")')
    DESCRIPTION = (AppiumBy.XPATH, '//*[contains(@text,"Descripción")]/following::android.widget.EditText[1]')

    def __init__(self, driver):
        super().__init__(driver)
        self.description_modified = None
        self.mobile_utils = MobileUtils(driver)
        self.menu_type_created = None

    def open_menutypes(self):
        self.click(self.MENU_TYPES)

    def create_new_menutype(self):
        self.menu_type_created = f"Carta QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.click(self.ADD_MENU_TYPE)
        self.write(self.NAME_MENU_TYPE, self.menu_type_created)
        for locator in (self.NEXT, self.STARTERS, self.PEPPERS, self.SALADS, self.SALAD_CESAR, self.NEXT, self.NEXT, self.FINISH_AND_SAVE):
            self.click(locator)

    def click_menutype_action(self, action):
        if not self.menu_type_created:
            raise Exception("No existe carta creada para buscar")
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.menu_type_created}")')
        menu_type = None
        for _ in range(8):
            try:
                menu_type = self.driver.find_element(*locator)
                if menu_type.is_displayed():
                    break
            except (NoSuchElementException, StaleElementReferenceException):
                pass
            self.mobile_utils.swipe_up()
        if menu_type is None or not menu_type.is_displayed():
            raise Exception(f"No se encontró la carta creada: {self.menu_type_created}")
        buttons = [element for element in self.driver.find_elements(*action) if element.is_displayed()]
        if not buttons:
            raise Exception(f"No se encontró el botón {action[1]} para {self.menu_type_created}")
        min(buttons, key=lambda element: abs(element.location["y"] - menu_type.location["y"])).click()
        return locator

    def delete_created_menutypes(self):
        self.click_menutype_action(self.BIN)
        self.click(self.DELETE)

    def modify_created_menutypes(self):
        locator = self.click_menutype_action(self.EDIT)
        self.description_modified = f"DescripcionQA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.write(self.DESCRIPTION, self.description_modified)
        for _ in range(3):
            self.click(self.NEXT)
        self.click(self.FINISH_AND_SAVE)
        self.wait_visibility(locator, timeout=WAIT_TIMEOUT)

    def verify_modification(self):
        self.click_menutype_action(self.SEE)
        self.wait_visibility(self.PREVIOUS, timeout=WAIT_TIMEOUT)
        time.sleep(1)
        self.click(self.PREVIOUS)
        description = self.wait_visibility(self.DESCRIPTION, timeout=WAIT_TIMEOUT)
        found_description = (description.get_attribute("text") or description.text or "").strip()
        print(f"Descripción esperada: {self.description_modified!r}")
        print(f"Descripción encontrada: {found_description!r}")
        if found_description != self.description_modified:
            raise AssertionError(f"La descripción no coincide: esperada={self.description_modified!r}, encontrada={found_description!r}")
        print(f"Modificación encontrada: {self.description_modified}")
        self.click(self.CLOSE)