from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from features.config.test_config import TEST_PASSWORD

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
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
        self.wait.until(EC.element_to_be_clickable(self.crear_cuenta)).click()

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
        self.wait.until(EC.visibility_of_element_located(self.usuario)).send_keys(usuario)
        self.wait.until(EC.visibility_of_element_located(self.email)).send_keys(email)
        self.wait.until(EC.visibility_of_element_located(self.password)).send_keys(password)
        self.wait.until(EC.visibility_of_element_located(self.repetir_password)).send_keys(password)
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        self.wait.until(EC.element_to_be_clickable(self.continuar)).click()
        self.wait.until(EC.visibility_of_element_located(self.restaurante)).send_keys(restaurante)
        self.wait.until(EC.element_to_be_clickable(self.continuar)).click()
        self.wait.until(EC.visibility_of_element_located(self.administrador)).send_keys(administrador)
        self.wait.until(EC.visibility_of_element_located(self.pin)).send_keys("QA1234")
        self.wait.until(EC.element_to_be_clickable(self.continuar)).click()
        self.wait.until(EC.visibility_of_element_located(self.plan)).click()
        self.wait.until(EC.element_to_be_clickable(self.crear_cuenta_entrar)).click()

    def crear_usuario(self):
        self.wait.until(EC.visibility_of_element_located(self.ventas))

    def comprobar_administrador_en_restaurante(self):
        self.wait.until(EC.visibility_of_element_located(self.ventas))
