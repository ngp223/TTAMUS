from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage

class RegisterPage(BasePage):
    CREAR_CUENTA = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-auth-page-auth-page--activation-1-div-auth-layout-1-div-auth-1-p-auth-switch-1-button-auth-switch__link-1")')
    USUARIO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-5")')
    REPETIR_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-6")')
    TIPO_NEGOCIO = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-auth-page-1-div-auth-layout-1-div-auth-1-tam-card-tam-card-1-div-auth-card__body-1-div-reg-business-1-tam-business-type-picker-1-div-biz-1-button-biz__item-1")')
    NOMBRE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-7")')
    TERRITORIO_FISCAL_DESPLEGABLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1-span-tam-select__value-1")')
    TERRITORIO_FISCAL_OPCION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1-opt-0")')
    CONTINUAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continuar")')
    RAZON_SOCIAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-10")')
    PLAN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-auth-page-1-div-auth-layout-1-div-auth-1-tam-card-tam-card-1-div-auth-card__body-1-div-plan-grid-1-button-plan-card-2")')
    ADMINISTRADOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-16")')
    EMAIL_ADMINISTRADOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-17")')
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
        self.click(self.CREAR_CUENTA)

    def rellenar_campos_obligatorios(self):
        password = TEST_PASSWORD
        fecha_hora = datetime.now().strftime('%d%m%Y%H%M%S')
        usuario = f"UsuarioQA_{fecha_hora}"
        email = f"{usuario}@sharklasers.com"
        nombre_comercial = f"NombreComercialQA_{fecha_hora}"
        razon_social = f"RazonSocialQA_{fecha_hora}"
        administrador = f"AdministradorQA_{fecha_hora}"
        email_administrador = f"{administrador}@sharklasers.com"
        self.usuario_creado = usuario
        self.email_creado = email
        self.password_creado = password
        self.administrador_creado = administrador
        self.administrador_inicial = administrador[0]
        self.escribir(self.USUARIO, nombre_comercial)
        self.escribir(self.EMAIL, email)
        self.escribir(self.PASSWORD, password)
        self.escribir(self.REPETIR_PASSWORD, password)
        self.click(self.TIPO_NEGOCIO)
        self.click(self.CONTINUAR)
        self.escribir(self.NOMBRE, nombre_comercial)
        self.click(self.TERRITORIO_FISCAL_DESPLEGABLE)
        self.click(self.TERRITORIO_FISCAL_OPCION)
        self.click(self.CONTINUAR)
        self.escribir(self.RAZON_SOCIAL, razon_social)
        self.click(self.CONTINUAR)
        self.click(self.PLAN)
        self.click(self.CONTINUAR)
        self.escribir(self.ADMINISTRADOR, administrador)
        self.escribir(self.EMAIL_ADMINISTRADOR, email_administrador)
        self.escribir(self.PIN, "DemoQA1234")
        self.click(self.CREAR_CUENTA_ENTRAR)

    def crear_usuario(self):
        self.esperar_visible(self.VENTAS)

    def comprobar_administrador_en_restaurante(self):
        self.esperar_visible(self.VENTAS)