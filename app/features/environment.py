import sys
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from features.pages.test_00_logout_page import LogoutPage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

APP_PACKAGE = "com.tamus.pos"
APP_ACTIVITY = "com.tamus.pos.MainActivity"
DEVICE_ID = "HA2ATXGT"
POPUP_REINTENTAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Reintentar")')
POPUP_CERRAR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cerrar")')
ACTIVAR_TERMINAL = (AppiumBy.XPATH, '//android.widget.Button[@text="Activar terminal"]')

def before_all(context):
    context.config.stdout_capture = False
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
    context.driver.terminate_app(APP_PACKAGE)
    context.driver.activate_app(APP_PACKAGE)
    cerrar_popups(context)
    cerrar_sesion_si_existe(context)

def cerrar_popups(context):
    for _ in range(3):
        cerrado = False
        for locator in (POPUP_REINTENTAR, POPUP_CERRAR):
            elementos = context.driver.find_elements(*locator)
            if elementos:
                try:
                    elementos[0].click()
                    cerrado = True
                    time.sleep(0.2)
                    break
                except Exception:
                    pass
        if not cerrado:
            break

def cerrar_sesion_si_existe(context):
    try:
        logout_page = LogoutPage(context.driver)
        if logout_page.logout_if_exists():
            cerrar_popups(context)
    except TimeoutException:
        pass
    except Exception:
        pass

def after_scenario(context, scenario):
    if context.logged_in:
        cerrar_popups(context)
        try:
            print("INICIANDO LOGOUT")
            logout_page = LogoutPage(context.driver)
            logout_page.logout()
            print("SALIR PULSADO")
            WebDriverWait(context.driver, 15).until(EC.presence_of_element_located(ACTIVAR_TERMINAL))
            print("ACTIVAR TERMINAL MOSTRADO")
        except Exception as e:
            print(f"ERROR LOGOUT: {e}")
            raise
    try:
        context.driver.terminate_app(APP_PACKAGE)
    except Exception:
        pass
def after_all(context):
    if hasattr(context, "driver") and context.driver:
        try:
            context.driver.quit()
        except Exception:
            pass