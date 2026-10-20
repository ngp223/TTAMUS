
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from datetime import datetime
import time


class CardsPage(BasePage):
    MENU_TYPES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cartas")')
    ADD_MENU_TYPE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Añadir Carta")')
    NAME_MENU_TYPE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
    NEXT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    STARTERS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Entrantes")')
    PEPPERS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("check_box_outline_blank Pimientos de Gernika")')
    SALADS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Ensaladas")')
    SALAD_CESAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("check_box_outline_blank Ensalada César")')
    FINISH_AND_SAVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Finalizar y Guardar")')
    BIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Eliminar")')
    DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')
    PREVIOUS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Anterior")')
    CLOSE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cerrar")')
    EDIT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Editar")')
    SEE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Ver")')

    def __init__(self, driver):
        super().__init__(driver)
        self.description_modified = None
        self.mobile_utils = MobileUtils(driver)
        self.menu_type_created = None

    def open_cards(self):
        self.click(self.MENU_TYPES)

    def create_new_card(self):
        self.menu_type_created = f"Carta QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.click(self.ADD_MENU_TYPE)
        self.write(self.NAME_MENU_TYPE, self.menu_type_created)
        self.click(self.NEXT)
        self.click(self.STARTERS)
        self.click(self.PEPPERS)
        self.click(self.SALADS)
        self.click(self.SALAD_CESAR)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click(self.FINISH_AND_SAVE)

    def scroll_to_created_card(self):
        if not self.menu_type_created:
            raise Exception("No existe carta creada para buscar")
        locator_menu_type = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.menu_type_created}")')
        for _ in range(8):
            try:
                menu_type = self.driver.find_element(*locator_menu_type)
                if menu_type.is_displayed():
                    return menu_type
            except Exception:
                pass
            self.scroll_cards_list()
        raise Exception(f"No se encontró la carta creada: {self.menu_type_created}")

    def scroll_cards_list(self):
        self.mobile_utils.swipe_up()

    def find_nearest_button(self, locator, menu_type, button_name):
        menu_type_pos = menu_type.location
        elements = self.driver.find_elements(*locator)
        if not elements:
            raise Exception(f"No se encontraron botones {button_name}")
        button_correct = None
        minimum_distance = float("inf")
        for element in elements:
            if not element.is_displayed():
                continue
            distance = abs(element.location["y"] - menu_type_pos["y"])
            if distance < minimum_distance:
                minimum_distance = distance
                button_correct = element
        if button_correct is None:
            raise Exception(f"No encontrado {button_name} para {self.menu_type_created}")
        return button_correct

    def delete_created_card(self):
        if not self.menu_type_created:
            raise Exception("No existe carta creada para borrar")
        menu_type = self.scroll_to_created_card()
        bin_correct = self.find_nearest_button(self.BIN, menu_type, "Eliminar")
        bin_correct.click()
        self.click(self.DELETE)

    def edit_menu_type_created(self):
        menu_type = self.scroll_to_created_card()
        edit_correct = self.find_nearest_button(self.EDIT, menu_type, "Editar")
        edit_correct.click()

    def field_below_label(self, label):
        return (
            AppiumBy.XPATH,f'//*[contains(@text,"{label}")]/following::android.widget.EditText[1]')

    def field_description(self):
        return self.field_below_label("Descripción")

    def modify_created_card(self):
        if not self.menu_type_created:
            raise Exception("No existe carta creada para modificar")
        self.edit_menu_type_created()
        self.description_modified = f"DescripcionQA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.write(self.field_description(), self.description_modified)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click(self.FINISH_AND_SAVE)
        locator_menu_type = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.menu_type_created}")')
        self.wait_visibility(locator_menu_type, timeout=15)

    def verify_modification(self):
        if not self.menu_type_created:
            raise Exception("No existe menu_type creada para verificar")
        menu_type = self.scroll_to_created_card()
        see_correct = self.find_nearest_button(self.SEE, menu_type, "Ver")
        see_correct.click()
        self.wait_visibility(self.PREVIOUS, timeout=10)
        time.sleep(1)
        self.click(self.PREVIOUS)
        description = self.wait_visibility(self.field_description(), timeout=10)
        value_description = (description.get_attribute("text") or description.text or "").strip()
        print(f"Descripción esperada: {self.description_modified!r}")
        print(f"Descripción encontrada: {value_description!r}")
        if value_description != self.description_modified:
            raise AssertionError(f"La descripción no coincide: esperada={self.description_modified!r}, encontrada={value_description!r}")
        print(f"Modificación encontrada: {self.description_modified}")
        self.click(self.CLOSE)
