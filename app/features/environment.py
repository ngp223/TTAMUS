import sys
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pages.E2E_00_login_page import LoginPage
from pages.E2E_00_home_page import HomePage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def before_all(context):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = "HA2ATXGT"
    options.app_package = "com.tamus.pos.staging"
    options.app_activity = "com.tamus.pos.MainActivity"
    options.no_reset = True
    options.full_reset = False
    context.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

def before_scenario(context, scenario):
    context.driver.terminate_app("com.tamus.pos.staging")
    context.driver.activate_app("com.tamus.pos.staging")
    if "E2E_01" in scenario.tags:
        preparar_registro(context.driver)
    else:
        LoginPage(context.driver).login()

def preparar_registro(driver):
    crear_cuenta = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Crear cuenta")')
    menu_usuario = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("A")')
    salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')
    try:
        WebDriverWait(driver, 3).until(lambda d: d.find_element(*crear_cuenta))
        return
    except TimeoutException:
        pass
    try:
        WebDriverWait(driver, 10).until(lambda d: d.find_element(*menu_usuario)).click()
        WebDriverWait(driver, 5).until(lambda d: d.find_element(*salir)).click()
        WebDriverWait(driver, 10).until(lambda d: d.find_element(*crear_cuenta))
    except TimeoutException:
        raise Exception("No se pudo preparar la aplicación para el registro")

def after_scenario(context, scenario):
    try:
        HomePage(context.driver).logout()
    except Exception as e:
        print(f"[WARN] No se pudo hacer logout: {e}")

def after_all(context):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()
