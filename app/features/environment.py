
import sys
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.logout_page import LogoutPage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

APP_PACKAGE = "com.tamus.pos"
APP_ACTIVITY = "com.tamus.pos.MainActivity"
DEVICE_ID = "HA2ATXGT"
POPUP_CLOSE = [
    (AppiumBy.ACCESSIBILITY_ID, "Descartar"),
    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cerrar")'),
    (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cerrar")')
]

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
    try:
        app_state = context.driver.query_app_state(APP_PACKAGE)
    except Exception:
        app_state = 1
    app_was_running = app_state in (2, 3, 4)
    context.driver.activate_app(APP_PACKAGE)
    time.sleep(1)
    close_popups(context)
    if app_was_running:
        logout_page = LogoutPage(context.driver)
        if logout_page.logout_if_exists():
            print("Sesión anterior cerrada correctamente")
        else:
            print("No se encontró una sesión iniciada; se continuará con el login")

def close_popups(context):
    driver = context.driver
    try:
        driver.switch_to.context("NATIVE_APP")
        for _ in range(5):
            closed = False
            for locator in POPUP_CLOSE:
                buttons = driver.find_elements(*locator)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        time.sleep(0.5)
                        closed = True
                        break
                if closed:
                    break
            if not closed:
                break
    finally:
        try:
            driver.switch_to.context("NATIVE_APP")
        except Exception:
            pass


def after_scenario(context, scenario):
    cleanup_error = None
    try:
        close_popups(context)
        if getattr(context, "logged_in", False):
            logout_page = LogoutPage(context.driver)
            logout_page.logout()
            print("Sesión cerrada correctamente al terminar el escenario")
    except Exception as e:
        cleanup_error = e
        print(f"ERROR al cerrar la sesión: {type(e).__name__}: {e}")
    finally:
        try:
            context.driver.switch_to.context("NATIVE_APP")
            context.driver.terminate_app(APP_PACKAGE)
            print("Aplicación cerrada al terminar el escenario")
        except Exception as e:
            print(f"ERROR al cerrar la aplicación: {type(e).__name__}: {e}")
            if cleanup_error is None:
                cleanup_error = e
    if cleanup_error is not None:
        raise cleanup_error


def after_all(context):
    if hasattr(context, "driver") and context.driver:
        try:
            context.driver.quit()
        except Exception:
            pass
