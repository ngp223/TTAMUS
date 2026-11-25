from datetime import datetime
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from features.config.test_config import WAIT_TIMEOUT, ZONE_SUPPLEMENT


class TablesMapPage(BasePage):
    TABLES_MAP = BasePage.by_text("Mapa de mesas")
    NEW_ZONE = BasePage.by_text("Nueva")
    ZONE_NAME = (AppiumBy.XPATH, '//*[contains(@text,"Nombre de la zona")]/following::android.widget.EditText[1]')
    CREATE_ZONE = BasePage.by_text("Crear Zona")
    RECTANGULAR_TABLE = BasePage.by_text_contains("Rectangular")
    TABLE = (AppiumBy.XPATH, '//*[contains(@resource-id,"div-canvas-1-div-mesa-")]')
    TABLE_NAME = (AppiumBy.XPATH, './/*[contains(@resource-id,"span-mesa__name")]')
    DELETE_TABLE = (AppiumBy.ACCESSIBILITY_ID, "Eliminar mesa")
    EDIT_ZONE = BasePage.by_text("Editar")
    DELETE_ZONE = BasePage.by_text("Eliminar")
    UPDATE_ZONE = BasePage.by_text("Actualizar")
    ZONE_ROW = '//*[starts-with(@resource-id,"cdk-drop-list-") and contains(@resource-id,"div-cdk-drag-") and .//*[@text="{zone_name}"]]'
    ZONE_MENU = (AppiumBy.XPATH, ZONE_ROW + '//*[@resource-id and contains(@resource-id,"button-tam-btn-")]')
    ZONE_TIMEOUT = 15
    ACTION_TIMEOUT = 2
    SAVE_TABLE_TEXT = "Guardar"
    TABLE_NAME_INPUT = BasePage.by_id("place-edit-name")
    UPDATED_TABLE_NAME = "Mesa QA"
    TABLE_EDIT_TIMEOUT = 15

    def __init__(self, driver):
        super().__init__(driver)
        self.created_zone = None
        self.updated_zone = None
        self.created_table_number = None

    def tables_map(self):
        self.click(self.TABLES_MAP)

    def create_zone(self):
        self.created_zone = f"Zona QA {datetime.now():%H%M%S_%d%m}"
        self.click(self.NEW_ZONE)
        self.write(self.ZONE_NAME, self.created_zone, timeout=self.ZONE_TIMEOUT)
        self.click(self.CREATE_ZONE, timeout=self.ZONE_TIMEOUT)
        time.sleep(self.ACTION_TIMEOUT)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(self.by_text(self.created_zone)))

    def create_table(self):
        self.click(self.RECTANGULAR_TABLE)
        table = self.wait_visibility(self.TABLE, timeout=WAIT_TIMEOUT)
        table_name = WebDriverWait(table, self.ZONE_TIMEOUT).until(EC.visibility_of_element_located(self.TABLE_NAME))
        self.created_table_number = table_name.text.strip()
        if not self.created_table_number:
            raise Exception("No se ha podido recuperar el número de la mesa creada")

    def modify_zone(self):
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(self.by_text(self.created_zone)))
        self.click((AppiumBy.XPATH, self.ZONE_MENU[1].format(zone_name=self.created_zone)), self.ZONE_TIMEOUT)
        self.click(self.EDIT_ZONE, self.ZONE_TIMEOUT)
        self.updated_zone = f"{self.created_zone} modificada"
        self.write(self.ZONE_NAME, self.updated_zone, timeout=self.ZONE_TIMEOUT)
        self.click(self.by_text_contains(ZONE_SUPPLEMENT), timeout=self.ZONE_TIMEOUT)
        self.click(self.UPDATE_ZONE, timeout=self.ZONE_TIMEOUT)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(self.by_text(self.updated_zone)))

    def modify_table(self):
        self.click(self.EDIT, timeout=self.ZONE_TIMEOUT)
        print("Pulsado el botón Editar mesa")
        time.sleep(self.ACTION_TIMEOUT)
        confirm_buttons = self.driver.find_elements(*self.EDIT)
        if confirm_buttons:
            confirm_buttons[-1].click()
        print("Dentro de la edicion")
        self.write(self.TABLE_NAME_INPUT, self.UPDATED_TABLE_NAME, timeout=self.TABLE_EDIT_TIMEOUT)
        self.click(self.by_text_contains(self.SAVE_TABLE_TEXT), timeout=self.TABLE_EDIT_TIMEOUT)
        print(f"Mesa modificada a {self.UPDATED_TABLE_NAME}")
        self.created_table_number = self.UPDATED_TABLE_NAME

    def delete_table(self):
        self.click(self.DELETE_TABLE, timeout=self.ZONE_TIMEOUT)
        print("Pulsado el botón Eliminar mesa")
        time.sleep(self.ACTION_TIMEOUT)
        confirm_buttons = self.driver.find_elements(*self.DELETE_TABLE)
        if confirm_buttons:
            confirm_buttons[-1].click()
        self.wait_invisibility(self.TABLE, timeout=self.ZONE_TIMEOUT)
        print("Mesa eliminada correctamente")

    def delete_zone(self):
        zone_name = self.updated_zone or self.created_zone
        zone_locator = self.by_text(zone_name)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(zone_locator))
        print(f"Zona localizada para borrar: {zone_name}")
        self.click((AppiumBy.XPATH, self.ZONE_MENU[1].format(zone_name=zone_name)), self.ZONE_TIMEOUT)
        self.confirm_delete(self.DELETE_ZONE, zone_locator, self.ZONE_TIMEOUT)
        print(f"Zona eliminada correctamente: {zone_name}")