
from datetime import datetime
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils

class TablesMapPage(BasePage):
    TABLES_MAP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Mapa de mesas")')
    NEW_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva")')
    ZONE_NAME = (AppiumBy.XPATH, '//*[contains(@text,"Nombre de la zona")]/following::android.widget.EditText[1]')
    CREATE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear Zona")')
    SAVE_ZONE = (AppiumBy.ID, 'cdk-dialog-2-tam-floor-edit-modal-1-tam-dialog-layout-tam-dialog-1-footer-tam-dialog__foot-1-button-tam-btn-2')
    TERRACE_SUPPLEMENT = (AppiumBy.ID, 'cdk-dialog-2-tam-floor-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-tam-form-stack-1-tam-field-tam-field-1-div-ze__fees-1-button-fee-2')
    RECTANGULAR_TABLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Rectangular")')
    ZOOM_IN = (AppiumBy.ID, 'tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-mapa-mesas-1-header-mapa__head-1-div-toolbar-1-div-toolbar__group-3-button-tam-btn-2')
    TABLE = (AppiumBy.XPATH, '//*[contains(@resource-id,"div-canvas-1-div-mesa-")]')
    TABLE_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("1")')
    TABLE_RESIZE_HANDLE = (AppiumBy.ID, 'tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-mapa-mesas-1-div-mapa__body-1-section-canvasarea-1-div-canvaswrap-1-div-canvasbox-1-div-canvas-1-div-mesa-1-span-sel-1-span-sel__h-2')
    DELETE_TABLE = (AppiumBy.ID, 'tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-mapa-mesas-1-div-mapa__body-1-section-canvasarea-1-div-canvaswrap-1-div-canvasbox-1-div-canvas-1-div-sel-bar-1-button-sel-bar__btn-2')
    EDIT_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')
    DELETE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')
    UPDATE_ZONE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Actualizar")')
    ZONE_ROW = '//*[starts-with(@resource-id,"cdk-drop-list-0-div-cdk-drag-") and .//*[@text="{zone_name}"]]'
    ZONE_MENU = (AppiumBy.XPATH, ZONE_ROW + '//*[@resource-id and contains(@resource-id,"button-tam-btn-1")]')
    ZONE_OPTION = (AppiumBy.XPATH, ZONE_ROW + '//*[@text="{option}"]')
    ZONE_TIMEOUT = 15
    ACTION_TIMEOUT = 2
    ZOOM_CLICKS = 3
    RESIZE_OFFSET_X = 80
    RESIZE_OFFSET_Y = 80
    GESTURE_SPEED = 800

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)
        self.created_zone = None
        self.updated_zone = None
        self.created_table = None

    def tables_map(self):
        self.click(self.TABLES_MAP)

    def create_zone(self):
        self.created_zone = f"Zona QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.click(self.NEW_ZONE)
        zone_name = WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.visibility_of_element_located(self.ZONE_NAME))
        zone_name.clear()
        zone_name.send_keys(self.created_zone)
        self.click(self.CREATE_ZONE, timeout=self.ZONE_TIMEOUT)
        time.sleep(self.ACTION_TIMEOUT)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located((AppiumBy.XPATH, self.ZONE_ROW.format(zone_name=self.created_zone))))

    def create_table(self):
        self.click(self.RECTANGULAR_TABLE)
        self.created_table = "1"
        time.sleep(self.ACTION_TIMEOUT)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(self.TABLE))
        print(f"Mesa creada y localizada en el mapa: {self.created_table}")

    def modify_zone(self):
        print(f"Buscando zona: {self.created_zone}")
        row_locator = (AppiumBy.XPATH, self.ZONE_ROW.format(zone_name=self.created_zone))
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(row_locator))
        print("Zona localizada")
        menu_locator = (AppiumBy.XPATH, self.ZONE_MENU[1].format(zone_name=self.created_zone))
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.element_to_be_clickable(menu_locator)).click()
        print("Menú de los tres puntos abierto")
        edit_locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.element_to_be_clickable(edit_locator)).click()
        print("Editar localizado y pulsado")
        zone_name = WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.visibility_of_element_located(self.ZONE_NAME))
        self.updated_zone = f"{self.created_zone} modificada"
        zone_name.clear()
        zone_name.send_keys(self.updated_zone)
        self.click((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Suplemento terraza")'), timeout=self.ZONE_TIMEOUT)
        self.click(self.UPDATE_ZONE, timeout=self.ZONE_TIMEOUT)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located((AppiumBy.XPATH, self.ZONE_ROW.format(zone_name=self.updated_zone))))
        print(f"Zona modificada: {self.updated_zone}")

    def modify_table(self):
        table_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_table}")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(table_locator))
        print("Mesa localizada")
        table = self.driver.find_element(*table_locator)
        table.click()
        for _ in range(self.ZOOM_CLICKS):
            self.click(self.ZOOM_IN)
        handle = WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.visibility_of_element_located(self.TABLE_RESIZE_HANDLE))
        handle_rect = handle.rect
        start_x = handle_rect["x"] + handle_rect["width"] // 2
        start_y = handle_rect["y"] + handle_rect["height"] // 2
        self.driver.execute_script("mobile: dragGesture", {"startX": start_x, "startY": start_y, "endX": start_x + self.RESIZE_OFFSET_X, "endY": start_y + self.RESIZE_OFFSET_Y, "speed": self.GESTURE_SPEED})
        time.sleep(self.ACTION_TIMEOUT)

    def delete_table(self):
        table_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_table}")')
        table = WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(table_locator))
        table.click()
        self.click(self.DELETE_TABLE)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.invisibility_of_element_located(table_locator))

    def delete_zone(self):
        zone_name = self.updated_zone or self.created_zone
        zone_locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{zone_name}")')
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.presence_of_element_located(zone_locator))
        print(f"Zona localizada para borrar: {zone_name}")
        menu_locator = (AppiumBy.XPATH, self.ZONE_MENU[1].format(zone_name=zone_name))
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.element_to_be_clickable(menu_locator)).click()
        self.click(self.DELETE_ZONE)
        WebDriverWait(self.driver, self.ZONE_TIMEOUT).until(EC.invisibility_of_element_located(zone_locator))
