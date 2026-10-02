from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from datetime import datetime
import time

class CardsPage(BasePage):
    CARTAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cartas")')
    ANADIR_CARTA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Añadir Carta")')
    NOMBRE_CARTA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
    SIGUIENTE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Siguiente")')
    ENTRANTES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Entrantes")')
    PIMIENTOS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("check_box_outline_blank Pimientos de Gernika")')
    ENSALADAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Ensaladas")')
    ENSALADA_CESAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("check_box_outline_blank Ensalada César")')
    FINALIZAR_Y_GUARDAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Finalizar y Guardar")')
    PAPELERA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Eliminar")')
    ELIMINAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Eliminar")')
    DESCRIPCION = (AppiumBy.XPATH, '//android.view.View[@text="DESCRIPCIÓN DE LA CARTA"]/following-sibling::android.view.View/android.widget.EditText')
    ANTERIOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Anterior")')
    CERRAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cerrar")')
    EDITAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Editar")')
    VER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Ver")')

    def __init__(self, driver):
        super().__init__(driver)
        self.carta_creada = None

    def open_cards(self):
        self.click(self.CARTAS)

    def create_new_card(self):
        self.carta_creada = f"Carta QA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.click(self.ANADIR_CARTA)
        self.escribir(self.NOMBRE_CARTA, self.carta_creada)
        self.click(self.SIGUIENTE)
        self.click(self.ENTRANTES)
        self.click(self.PIMIENTOS)
        self.click(self.ENSALADAS)
        self.click(self.ENSALADA_CESAR)
        self.click(self.SIGUIENTE)
        self.click(self.SIGUIENTE)
        self.click(self.FINALIZAR_Y_GUARDAR)

    def scroll_to_created_card(self):
        if not self.carta_creada:
            raise Exception("No existe carta creada para buscar")
        locator_carta = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.carta_creada}")')
        for _ in range(8):
            try:
                carta = self.driver.find_element(*locator_carta)
                if carta.is_displayed():
                    return carta
            except Exception:
                pass
            self.scroll_cards_list()
        raise Exception(f"No se encontró la carta creada: {self.carta_creada}")

    def scroll_cards_list(self):
        size = self.driver.get_window_size()
        width = size["width"]
        height = size["height"]
        x = width // 2
        start_y = int(height * 0.80)
        end_y = int(height * 0.35)
        self.driver.swipe(x, start_y, x, end_y, 600)

    def delete_created_card(self):
        if not self.carta_creada:
            raise Exception("No existe carta creada para borrar")
        carta = self.scroll_to_created_card()
        carta_pos = carta.location
        papeleras = self.driver.find_elements(*self.PAPELERA)
        if not papeleras:
            raise Exception("No se encontraron papeleras")
        papelera_correcta = None
        distancia_minima = float("inf")
        for papelera in papeleras:
            if not papelera.is_displayed():
                continue
            papelera_pos = papelera.location
            distancia = abs(papelera_pos["y"] - carta_pos["y"])
            if distancia < distancia_minima:
                distancia_minima = distancia
                papelera_correcta = papelera
        if papelera_correcta is None:
            raise Exception(f"No encontrada papelera para {self.carta_creada}")
        papelera_correcta.click()
        self.click(self.ELIMINAR)

    def modify_created_card(self):
        if not self.carta_creada:
            raise Exception("No existe carta creada para modificar")
        carta = self.scroll_to_created_card()
        carta_pos = carta.location
        elementos_editar = self.driver.find_elements(*self.EDITAR)
        if not elementos_editar:
            raise Exception("No se encontraron botones Editar")
        editar_correcto = None
        distancia_minima = float("inf")
        for editar in elementos_editar:
            if not editar.is_displayed():
                continue
            editar_pos = editar.location
            distancia = abs(editar_pos["y"] - carta_pos["y"])
            if distancia < distancia_minima:
                distancia_minima = distancia
                editar_correcto = editar
        if editar_correcto is None:
            raise Exception(f"No encontrado Editar para {self.carta_creada}")
        editar_correcto.click()
        self.descripcion_modificada = f"DescripcionQA {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.escribir(self.DESCRIPCION, self.descripcion_modificada)
        self.click(self.SIGUIENTE)
        self.click(self.SIGUIENTE)
        self.click(self.SIGUIENTE)
        self.click(self.FINALIZAR_Y_GUARDAR)
        locator_carta = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.carta_creada}")')
        self.esperar_visible(locator_carta, timeout=15)

    def verify_modification(self):
        if not self.carta_creada:
            raise Exception("No existe carta creada para verificar")
        carta = self.scroll_to_created_card()
        carta_pos = carta.location
        elementos_ver = self.driver.find_elements(*self.VER)
        if not elementos_ver:
            raise Exception(f"No se encontraron botones Ver para {self.carta_creada}")
        ver_correcto = None
        distancia_minima = float("inf")
        for ver in elementos_ver:
            if not ver.is_displayed():
                continue
            ver_pos = ver.location
            distancia = abs(ver_pos["y"] - carta_pos["y"])
            if distancia < distancia_minima:
                distancia_minima = distancia
                ver_correcto = ver
        if ver_correcto is None:
            raise Exception(f"No encontrado Ver para {self.carta_creada}")
        ver_correcto.click()
        self.esperar_visible(self.ANTERIOR, timeout=10)
        time.sleep(1)
        self.click(self.ANTERIOR)
        descripcion = self.esperar_visible(self.DESCRIPCION, timeout=10)
        valor_descripcion = (descripcion.get_attribute("text") or descripcion.text or "").strip()
        print(f"Descripción esperada: {self.descripcion_modificada!r}")
        print(f"Descripción encontrada: {valor_descripcion!r}")
        if valor_descripcion != self.descripcion_modificada:
            raise AssertionError(f"La descripción no coincide: esperada={self.descripcion_modificada!r}, encontrada={valor_descripcion!r}")
        print(f"Modificación encontrada: {self.descripcion_modificada}")
        self.click(self.CERRAR)