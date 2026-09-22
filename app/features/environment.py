import sys
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

APP_PACKAGE = "com.tamus.pos"
APP_ACTIVITY = "com.tamus.pos.MainActivity"
DEVICE_ID = "HA2ATXGT"

def before_all(context):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = DEVICE_ID
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    options.full_reset = False
    context.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

def before_scenario(context, scenario):
    context.logged_in = False
    context.user_initial = None
    context.driver.terminate_app(APP_PACKAGE)
    context.driver.activate_app(APP_PACKAGE)
    cerrar_sesion_si_existe(context)

def cerrar_sesion_si_existe(context):
    wait = WebDriverWait(context.driver, 3)
    try:
        inicial = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("[A-Z]")')))
        inicial.click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")'))).click()
        WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Crear cuenta")')))
    except TimeoutException:
        pass

def after_scenario(context, scenario):
    if context.logged_in and context.user_initial:
        try:
            wait = WebDriverWait(context.driver, 10)
            inicial = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{context.user_initial}")')
            salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')
            wait.until(EC.element_to_be_clickable(inicial)).click()
            wait.until(EC.element_to_be_clickable(salir)).click()
        except Exception as e:
            print(f"[WARN] No se pudo hacer logout: {e}")
    try:
        context.driver.terminate_app(APP_PACKAGE)
    except Exception as e:
        print(f"[WARN] No se pudo cerrar la app: {e}")

def after_all(context):
    if hasattr(context, "driver") and context.driver:
        try:
            context.driver.quit()
        except Exception as e:
            print(f"[WARN] No se pudo cerrar el driver: {e}")
