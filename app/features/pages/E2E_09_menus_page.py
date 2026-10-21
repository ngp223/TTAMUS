from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from datetime import datetime

class MenusPage(BasePage):
    MENUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Menús")')
    NEW_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nuevo Menú")')
    MENU_NAME = (AppiumBy.XPATH, '//*[contains(@text,"Nombre del menú")]/following::android.widget.EditText[1]')
    NEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    SECTION_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-button-tam-btn-1")')
    SECTION_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-button-tam-btn-1")')
    SECTION_3 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-button-tam-btn-1")')
    TORTILLA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-picker-1-div-picker__list-1-button-picker__item-4")')
    OCTOPUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-div-picker-1-div-picker__list-1-button-picker__item-2")')
    SECTION_1_DONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    SECTION_2_DONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    SECTION_3_DONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    SEARCH_DESSERT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-12")')
    CHEESECAKE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-div-picker-1-div-picker__list-1-button-picker__item-1")')
    CREATE_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear Menú")')
    MAXIMUM = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-1-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-section__head-1-div-section__max-1-input-section__max-input-1")')
    NEW_MAXIMUM = "3"
    SAVE_CHANGES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-1-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-footer-tam-dialog__foot-1-button-tam-btn-2")')
    EDIT = [(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Editar")'), (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')]
    TRASH = [(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Eliminar")'), (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Borrar")')]
    DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)
        self.created_menu = None
        self.modified_description = None

    def open_menus(self):
        self.click(self.MENUS)

    def create_menu(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.created_menu = f"Menu diario QA {timestamp}"
        self.click(self.NEW_MENU)
        self.write(self.MENU_NAME, self.created_menu)
        self.click(self.NEXT)
        self.click(self.SECTION_1)
        self.click(self.TORTILLA)
        self.click(self.SECTION_1_DONE)
        self.mobile_utils.swipe_up()
        self.click(self.SECTION_2)
        self.click(self.OCTOPUS)
        self.click(self.SECTION_2_DONE)
        self.click(self.SECTION_3)
        self.write(self.SEARCH_DESSERT, "Tarta")
        self.click(self.CHEESECAKE)
        self.click(self.SECTION_3_DONE)
        self.click(self.CREATE_MENU)
        self.find_menu()

    def find_menu(self):
        if not self.created_menu:
            raise Exception("No existe menu")
        menu_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_menu}")')
        for _ in range(8):
            try:
                menu = self.driver.find_element(*menu_locator)
                if menu.is_displayed():
                    return menu
            except Exception:
                pass
            self.mobile_utils.swipe_up()
        raise Exception(f"Created menu not found: {self.created_menu}")

    def find_menu_action(self, locators):
        menu = self.find_menu()
        menu_y = menu.location["y"]
        elements = []
        for locator in locators:
            try:
                elements.extend(self.driver.find_elements(*locator))
            except Exception:
                pass
        if not elements:
            raise Exception(f"No buttons found for menu {self.created_menu}")
        target_element = None
        min_distance = float("inf")
        for element in elements:
            if not element.is_displayed():
                continue
            distance = abs(element.location["y"] - menu_y)
            if distance < min_distance:
                min_distance = distance
                target_element = element
        if target_element is None:
            raise Exception(f"Corresponding action not found for menu {self.created_menu}")
        return target_element

    def modify_menu(self):
        edit_element = self.find_menu_action(self.EDIT)
        edit_element.click()
        self.modified_description = f"Menu diario QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.write(self.MENU_NAME, self.modified_description)
        self.click(self.NEXT)
        self.click(self.SAVE_CHANGES)
        self.created_menu = self.modified_description

    def verify_modified_menu(self):
        self.created_menu = self.modified_description
        self.find_menu()

    def delete_menu(self):
        trash_element = self.find_menu_action(self.TRASH)
        trash_element.click()
        self.click(self.DELETE)
