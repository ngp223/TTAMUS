from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from datetime import datetime

class MenusPage(BasePage):
    MENUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Menús")')
    NEW_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nuevo Menú")')
    MENU_NAME = (AppiumBy.XPATH, '//*[contains(@text,"Nombre del menú")]/following::android.widget.EditText[1]')
    NEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    SECTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-{number}-button-tam-btn-1")')
    SECTION_DONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-{number}-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    TORTILLA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-picker-1-div-picker__list-1-button-picker__item-4")')
    OCTOPUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-div-picker-1-div-picker__list-1-button-picker__item-2")')
    SEARCH_DESSERT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-12")')
    CHEESECAKE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-div-picker-1-div-picker__list-1-button-picker__item-1")')
    CREATE_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear Menú")')
    SAVE_CHANGES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-1-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-footer-tam-dialog__foot-1-button-tam-btn-2")')
    EDIT = [(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Editar")'), (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')]
    TRASH = [(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Eliminar")'), (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Borrar")')]
    DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)
        self.created_menu = None
        self.modified_description = None

    def section(self, number):
        return self.SECTION[0], self.SECTION[1].format(number=number)

    def section_done(self, number):
        return self.SECTION_DONE[0], self.SECTION_DONE[1].format(number=number)

    def open_menus(self):
        self.click(self.MENUS)

    def create_menu(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.created_menu = f"Menu diario QA {timestamp}"
        self.click(self.NEW_MENU)
        self.write(self.MENU_NAME, self.created_menu)
        self.click(self.NEXT)
        self.click(self.section(1))
        self.click(self.TORTILLA)
        self.click(self.section_done(1))
        self.mobile_utils.swipe_up()
        self.click(self.section(2))
        self.click(self.OCTOPUS)
        self.click(self.section_done(2))
        self.click(self.section(3))
        self.write(self.SEARCH_DESSERT, "Tarta")
        self.click(self.CHEESECAKE)
        self.click(self.section_done(3))
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
        menu_id = menu.get_attribute("resource-id")
        if not menu_id:
            raise Exception(f"No se pudo obtener el resource-id del menú {self.created_menu}")
        row_id = menu_id.split("-div-row__content-1-span-col-1")[0]
        for locator in locators:
            for element in self.driver.find_elements(*locator):
                element_id = element.get_attribute("resource-id") or ""
                if element.is_displayed() and element.is_enabled() and element_id.startswith(row_id + "-span-col-1-button-"):
                    return element
        raise Exception(f"No se encontró la acción para el menú {self.created_menu}")

    def modify_menu(self):
        edit_element = self.find_menu_action(self.EDIT)
        edit_element.click()
        self.modified_description = f"Menu diario QA {datetime.now().strftime('%Y%m%d_%H%M%S')} modificado"
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