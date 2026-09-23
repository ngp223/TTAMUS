from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.crear_cuenta = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Crear cuenta")')
        self.usuario = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
        self.email = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
        self.password = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-5")')
        self.repetir_password = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-6")')
        self.continuar = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continuar")')
        self.restaurante = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-13")')
        self.administrador = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-16")')
        self.plan = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Basic 19 € / mes Local, offline y con respaldo fiscal al reconectar.")')
        self.pin = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-18")')
        self.crear_cuenta_entrar = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear cuenta y entrar")')
        self.ventas = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("VENTAS")')
        self.usuario_creado = None
        self.email_creado = None
        self.password_creado = None
        self.administrador_creado = None
        self.administrador_inicial = None

    def click_crear_cuenta(self):
        self.scroll_hasta_texto("Crear cuenta")
        self.click(self.crear_cuenta)

    def rellenar_campos_obligatorios(self):
        password = TEST_PASSWORD
        fecha_hora = datetime.now().strftime('%d%m%Y%H%M%S')
        usuario = f"UsuarioQA_{fecha_hora}"
        email = f"{usuario}@sharklasers.com"
        restaurante = f"RestauranteQA_{fecha_hora}"
        administrador = f"AdministradorQA_{fecha_hora}"
        #usuario = f"UsuarioQA"
        #email = TEST_EMAIL
        #restaurante = f"RestauranteQA"
        #administrador = f"AdministradorQA"
        self.usuario_creado = usuario
        self.email_creado = email
        self.password_creado = password
        self.administrador_creado = administrador
        self.administrador_inicial = administrador[0]
        self.escribir(self.usuario, usuario)
        self.escribir(self.email, email)
        self.escribir(self.password, password)
        self.escribir(self.repetir_password, password)
        self.scroll_hasta_texto("Continuar")
        self.click(self.continuar)
        self.escribir(self.restaurante, restaurante)
        self.click(self.continuar)
        self.escribir(self.administrador, administrador)
        self.escribir(self.pin, "QA1234")
        self.click(self.continuar)
        self.click(self.plan)
        self.click(self.crear_cuenta_entrar)

    def crear_usuario(self):
        self.esperar_visible(self.ventas)

    def comprobar_administrador_en_restaurante(self):
        self.esperar_visible(self.ventas)
