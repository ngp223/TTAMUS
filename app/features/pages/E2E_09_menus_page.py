from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.mobile_utils import MobileUtils
from datetime import datetime

class MenusPage(BasePage):
    CARTAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Menús")')
    NUEVO_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nuevo Menú")')
    NOMBRE_MENU = (AppiumBy.XPATH, '//*[contains(@text,"Nombre del menú")]/following::android.widget.EditText[1]')
    SIGUIENTE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    SECCION_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-button-tam-btn-1")')
    SECCION_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-button-tam-btn-1")')
    SECCION_3 = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-button-tam-btn-1")')
    TORTILLA = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-picker-1-div-picker__list-1-button-picker__item-4")')
    PULPO = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-div-picker-1-div-picker__list-1-button-picker__item-2")')
    LISTO_SECCION_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    LISTO_SECCION_2 = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-2-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    LISTO_SECCION_3 = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-div-picker-1-div-picker__top-1-button-tam-btn-2")')
    BUSCAR_PRODUCTO_POSTRE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-12")')
    TARTA_QUESO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-0-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-3-div-picker-1-div-picker__list-1-button-picker__item-1")')
    CREAR_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear Menú")')
    MAXIMO = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("cdk-dialog-1-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-div-tam-dialog__body-1-div-section-1-div-section__head-1-div-section__max-1-input-section__max-input-1")')
    MAXIMO_NUEVO = "3"
    GUARDAR_CAMBIOS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-1-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-footer-tam-dialog__foot-1-button-tam-btn-2")')
    GUARDAR_CAMBIOS2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("cdk-dialog-1-tam-menu-edit-modal-1-tam-dialog-layout-tam-dialog-1-footer-tam-dialog__foot-1-button-tam-btn-2")')
    EDITAR = [(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Editar")'), (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Editar")')]
    PAPELERA = [(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Eliminar")'), (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Borrar")')]
    ELIMINAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')

    def __init__(self, driver):
        super().__init__(driver)
        self.mobile_utils = MobileUtils(driver)
        self.menu_creado = None
        self.descripcion_modificada = None

    def acceder_menus(self):
        self.click(self.CARTAS)

    def crear_menu(self):
        fecha_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.menu_creado = f"Menu diario QA {fecha_hora}"
        self.click(self.NUEVO_MENU)
        self.escribir(self.NOMBRE_MENU, self.menu_creado)
        self.click(self.SIGUIENTE)
        self.click(self.SECCION_1)
        self.click(self.TORTILLA)
        self.click(self.LISTO_SECCION_1)
        self.mobile_utils.swipe_up()
        self.click(self.SECCION_2)
        self.click(self.PULPO)
        self.click(self.LISTO_SECCION_2)
        self.click(self.SECCION_3)
        self.escribir(self.BUSCAR_PRODUCTO_POSTRE, "Tarta")
        self.click(self.TARTA_QUESO)
        self.click(self.LISTO_SECCION_3)
        self.click(self.CREAR_MENU)
        self.localizar_menu()

    def localizar_menu(self):
        if not self.menu_creado:
            raise Exception("No existe menú creado para buscar")
        locator_menu = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.menu_creado}")')
        for _ in range(8):
            try:
                menu = self.driver.find_element(*locator_menu)
                if menu.is_displayed():
                    return menu
            except Exception:
                pass
            self.mobile_utils.swipe_up()
        raise Exception(f"No se encontró el menú creado: {self.menu_creado}")

    def localizar_accion_menu(self, locators):
        menu = self.localizar_menu()
        menu_y = menu.location["y"]
        elementos = []
        for locator in locators:
            try:
                elementos.extend(self.driver.find_elements(*locator))
            except Exception:
                pass
        if not elementos:
            raise Exception(f"No se encontraron botones para el menú {self.menu_creado}")
        elemento_correcto = None
        distancia_minima = float("inf")
        for elemento in elementos:
            if not elemento.is_displayed():
                continue
            distancia = abs(elemento.location["y"] - menu_y)
            if distancia < distancia_minima:
                distancia_minima = distancia
                elemento_correcto = elemento
        if elemento_correcto is None:
            raise Exception(f"No se encontró la acción correspondiente al menú {self.menu_creado}")
        return elemento_correcto

    def obtener_valor(self, campo):
        return (campo.get_attribute("text") or campo.get_attribute("value") or campo.text or "").strip()

    def modificar_menu(self):
        elemento_editar = self.localizar_accion_menu(self.EDITAR)
        elemento_editar.click()
        campo_nombre = self.esperar_visible(self.NOMBRE_MENU, timeout=15)
        nombre_actual = self.obtener_valor(campo_nombre)
        self.descripcion_modificada = f"{nombre_actual} modificado".strip()
        self.escribir(self.NOMBRE_MENU, self.descripcion_modificada)
        self.click(self.SIGUIENTE)
        self.click(self.GUARDAR_CAMBIOS2)
        self.menu_creado = self.descripcion_modificada

    def comprobar_menu_modificado(self):
        self.menu_creado = self.descripcion_modificada
        self.localizar_menu()

    def borrar_menu(self):
        elemento_papelera = self.localizar_accion_menu(self.PAPELERA)
        elemento_papelera.click()
        self.click(self.ELIMINAR)