from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
import time


class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.crear_cuenta = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear cuenta")')
        self.usuario = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
        self.email = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
        self.password = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-5")')
        self.repetir_password = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-6")')
        self.continuar = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continuar")')
        self.restaurante = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-13")')
        self.administrador = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-16")')
        self.pin = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-18")')
        self.crear_cuenta_entrar = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear cuenta y entrar")')
        self.ventas = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("VENTAS")')

    def click_crear_cuenta(self):
        self.driver.find_element(*self.crear_cuenta).click()
        time.sleep(2)

    def rellenar_campos_obligatorios(self):
        fecha_hora = datetime.now().strftime('%d%m%Y%H%M%S')
        usuario = f"UsuarioQA{fecha_hora}"
        email = f"{usuario}@sharklasers.com"
        password = f"{usuario}123"
        restaurante = f"RestauranteQA{fecha_hora}"
        administrador = f"Administrador{fecha_hora}"
        self.usuario_creado = usuario
        self.email_creado = email
        self.password_creado = password
        self.driver.find_element(*self.usuario).send_keys(usuario)
        self.driver.find_element(*self.email).send_keys(email)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.repetir_password).send_keys(password)
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()')
        self.driver.find_element(*self.continuar).click()
        time.sleep(2)
        self.driver.find_element(*self.restaurante).send_keys(restaurante)
        self.driver.find_element(*self.continuar).click()
        time.sleep(2)
        self.driver.find_element(*self.administrador).send_keys(administrador)
        self.driver.find_element(*self.pin).send_keys("1234")
        self.driver.find_element(*self.continuar).click()
        time.sleep(2)
        self.driver.find_element(*self.crear_cuenta_entrar).click()
        time.sleep(2)

    def crear_usuario(self):
        pass

    def comprobar_administrador_en_restaurante(self):
        self.driver.find_element(*self.ventas)
