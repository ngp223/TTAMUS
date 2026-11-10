from datetime import datetime
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from features.config.test_config import WAIT_TIMEOUT


class TablesMapPage(BasePage):
    TABLES_MAP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Mapa de mesas")')
    NEW_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva")')
    ZONE_NAME = (AppiumBy.XPATH, '//*[contains(@text,"Nombre de la zona")]/following::android.widget.EditText[1]')
    CREATE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear Zona")')
    RECTANGULAR_TABLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Rectangular")')
    TABLE = (AppiumBy.XPATH, '//*[contains(@resource-id,"div-canvas-1-div-mesa-")]')
    TABLE_NAME = (AppiumBy.XPATH, './/*[contains(@resource-id,"span-mesa__name")]')
    TABLE_BY_NUMBER = (AppiumBy.XPATH,'//*[contains(@resource-id,"div-canvas-1-div-mesa-")] [.//*[contains(@resource-id,"span-mesa__name") and normalize-space()="{table_number}"]]')
    EDIT_TABLE = (AppiumBy.ACCESSIBILITY_ID, "Editar")
    DELETE_TABLE = (AppiumBy.ACCESSIBILITY_ID, "Eliminar mesa")
    EDIT_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')
    DELETE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')
    CONFIRM_DELETE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')
    UPDATE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Actualizar")')
    ZONE_ROW = '//*[starts-with(@resource-id,"cdk-drop-list-") and contains(@resource-id,"div-cdk-drag-") and .//*[@text="{zone_name}"]]'
    ZONE_MENU = (AppiumBy.XPATH, ZONE_ROW + '//*[@resource-id and contains(@resource-id,"button-tam-btn-")]')
    ZONE_OPTION = (AppiumBy.XPATH, ZONE_ROW + '//*[@text="{option}"]')
    ZONE_TIMEOUT = 15
    ACTION_TIMEOUT = 2
    SAVE_TABLE_TEXT = "Guardar"
    TABLE_NAME_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("place-edit-name")')
    UPDATED_TABLE_NAME = "Mesa QA"
    TABLE_EDIT_TIMEOUT = 15

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)
        self.created_zone = None
        self.updated_zone = None
        self.created_table = None
        self.created_table_number = None
        self.created_table_locator = None

    def tables_map(self):
        self.click(self.TABLES_MAP)

    def create_zone(self):
        self.created_zone = f"Zona QA {datetime.now().strftime('%H%M%S_%d%m')}"
        self.click(self.NEW_ZONE)
        zone_name = WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.visibility_of_element_located(self.ZONE_NAME))
        zone_name.clear()
        zone_name.send_keys(self.created_zone)
        self.click(self.CREATE_ZONE, timeout=self.ZONE_TIMEOUT)
        time.sleep(self.ACTION_TIMEOUT)
        exact_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_zone}")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(exact_locator))

    def create_table(self):
        self.click(self.RECTANGULAR_TABLE)
        table = WebDriverWait(self.driver, WAIT_TIMEOUT).until(EC.visibility_of_element_located(self.TABLE))
        table_name = WebDriverWait(table, self.ZONE_TIMEOUT).until(EC.visibility_of_element_located(self.TABLE_NAME))
        self.created_table = table_name.text.strip()
        self.created_table_number = self.created_table
        if not self.created_table_number:
            raise Exception("No se ha podido recuperar el número de la mesa creada")
        self.created_table_locator = (
        self.TABLE_BY_NUMBER[0], self.TABLE_BY_NUMBER[1].format(table_number=self.created_table_number))

    def modify_zone(self):
        zone_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_zone}")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(zone_locator))
        row_locator = (AppiumBy.XPATH, self.ZONE_ROW.format(zone_name=self.created_zone))
        menu_locator = (AppiumBy.XPATH, self.ZONE_MENU[1].format(zone_name=self.created_zone))
        print("CONTEXTO:", self.driver.current_context)
        print("ZONA:", self.created_zone)
        print("ZONA ENCONTRADA:", len(self.driver.find_elements(*zone_locator)))
        print("FILA ENCONTRADA:", len(self.driver.find_elements(*row_locator)))
        print("MENU ENCONTRADO:", len(self.driver.find_elements(*menu_locator)))
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.element_to_be_clickable(menu_locator)).click()
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.element_to_be_clickable(self.EDIT_ZONE)).click()
        zone_name = WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(
            EC.visibility_of_element_located(self.ZONE_NAME))
        self.updated_zone = f"{self.created_zone} modificada"
        zone_name.clear()
        zone_name.send_keys(self.updated_zone)
        self.click((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Suplemento terraza")'),
                   timeout=self.ZONE_TIMEOUT)
        self.click(self.UPDATE_ZONE, timeout=self.ZONE_TIMEOUT)
        updated_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.updated_zone}")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(updated_locator))
    def modify_table(self):
        self.click(self.EDIT_TABLE, timeout=self.ZONE_TIMEOUT)
        print("Pulsado el botón Editar mesa")
        time.sleep(self.ACTION_TIMEOUT)
        confirm_buttons = self.driver.find_elements(*self.EDIT_TABLE)
        if confirm_buttons:
            confirm_buttons[-1].click()
        print("Dentro de la edicion")
        table_input = WebDriverWait(self.driver, self.TABLE_EDIT_TIMEOUT).until(EC.visibility_of_element_located(self.TABLE_NAME_INPUT))
        table_input.clear()
        table_input.send_keys(self.UPDATED_TABLE_NAME)
        save_button = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{self.SAVE_TABLE_TEXT}")')
        self.click(save_button, timeout=self.TABLE_EDIT_TIMEOUT)
        print(f"Mesa modificada a {self.UPDATED_TABLE_NAME}")
        self.created_table_number = self.UPDATED_TABLE_NAME

    def delete_table(self):
        self.click(self.DELETE_TABLE, timeout=self.ZONE_TIMEOUT)
        print("Pulsado el botón Eliminar mesa")
        time.sleep(self.ACTION_TIMEOUT)
        confirm_buttons = self.driver.find_elements(*self.DELETE_TABLE)
        if confirm_buttons:
            confirm_buttons[-1].click()
        print("Eliminación de mesa ejecutada")

    def delete_zone(self):
        zone_name = self.updated_zone or self.created_zone
        zone_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{zone_name}")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(zone_locator))
        print(f"Zona localizada para borrar: {zone_name}")
        menu_locator = (AppiumBy.XPATH, self.ZONE_MENU[1].format(zone_name=zone_name))
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.element_to_be_clickable(menu_locator)).click()
        self.click(self.DELETE_ZONE, timeout=self.ZONE_TIMEOUT)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(
            EC.element_to_be_clickable(self.CONFIRM_DELETE_ZONE)).click()
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.invisibility_of_element_located(zone_locator))
        print(f"Zona eliminada correctamente: {zone_name}")
