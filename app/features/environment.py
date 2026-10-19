import sys
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from features.pages.logout_page import LogoutPage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

APP_PACKAGE = "com.tamus.pos"
APP_ACTIVITY = "com.tamus.pos.MainActivity"
DEVICE_ID = "HA2ATXGT"
POPUP_RETRY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Reintentar")')
POPUP_CLOSE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cerrar")')
POPUP_ERROR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Ha ocurrido un error. Inténtalo de nuevo")')
POPUP_DISMISS = (AppiumBy.ACCESSIBILITY_ID, "Descartar")
ACTIVE_TERMINAL = (AppiumBy.XPATH, '//android.widget.Button[@text="Activar terminal"]')


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
    close_popups(context)
    context.driver.terminate_app(APP_PACKAGE)
    time.sleep(1)
    context.driver.activate_app(APP_PACKAGE)
    time.sleep(2)
    close_popups(context)
    close_sesion_if_exist(context)


def close_popups(context):
    driver = context.driver
    try:
        driver.switch_to.context("NATIVE_APP")
        for intento in range(5):
            botones = driver.find_elements(*POPUP_DISMISS)
            if not botones:
                break
            botones[0].click()
            time.sleep(0.3)
    finally:
        try:
            driver.switch_to.context("NATIVE_APP")
        except Exception:
            pass


def close_sesion_if_exist(context):
    try:
        logout_page = LogoutPage(context.driver)
        if logout_page.logout_if_exists():
            close_popups(context)
    except TimeoutException:
        pass
    except Exception:
        pass


def after_scenario(context, scenario):
    if context.logged_in:
        close_popups(context)
        try:
            logout_page = LogoutPage(context.driver)
            logout_page.logout()
            WebDriverWait(context.driver, 15).until(
                EC.presence_of_element_located(ACTIVE_TERMINAL)
            )
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