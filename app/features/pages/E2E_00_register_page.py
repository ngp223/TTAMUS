from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage


class RegisterPage(BasePage):
    CREAR_CUENTA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Crear cuenta")')
    USUARIO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-5")')
    REPETIR_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-6")')
    CONTINUAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continuar")')
    RESTAURANTE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-13")')
    ADMINISTRADOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-16")')
    PLAN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Basic 19 € / mes Local, offline y con respaldo fiscal al reconectar.")')
    PIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-18")')
    CREAR_CUENTA_ENTRAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear cuenta y entrar")')
    VENTAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("VENTAS")')

    def __init__(self, driver):
        super().__init__(driver)
        self.usuario_creado = None
        self.email_creado = None
        self.password_creado = None
        self.administrador_creado = None
        self.administrador_inicial = None

    def click_crear_cuenta(self):
        self.scroll_hasta_texto("Crear cuenta")
        self.click(self.CREAR_CUENTA)

    def rellenar_campos_obligatorios(self):
        password = TEST_PASSWORD
        fecha_hora = datetime.now().strftime('%d%m%Y%H%M%S')
        usuario = f"UsuarioQA_{fecha_hora}"
        email = f"{usuario}@sharklasers.com"
        restaurante = f"RestauranteQA_{fecha_hora}"
        administrador = f"AdministradorQA_{fecha_hora}"
        self.usuario_creado = usuario
        self.email_creado = email
        self.password_creado = password
        self.administrador_creado = administrador
        self.administrador_inicial = administrador[0]
        self.escribir(self.USUARIO, usuario)
        self.escribir(self.EMAIL, email)
        self.escribir(self.PASSWORD, password)
        self.escribir(self.REPETIR_PASSWORD, password)
        self.scroll_hasta_texto("Continuar")
        self.click(self.CONTINUAR)
        self.escribir(self.RESTAURANTE, restaurante)
        self.click(self.CONTINUAR)
        self.escribir(self.ADMINISTRADOR, administrador)
        self.escribir(self.PIN, "QA1234")
        self.click(self.CONTINUAR)
        self.click(self.PLAN)
        self.click(self.CREAR_CUENTA_ENTRAR)

    def crear_usuario(self):
        self.esperar_visible(self.VENTAS)

    def comprobar_administrador_en_restaurante(self):
        self.esperar_visible(self.VENTAS)
