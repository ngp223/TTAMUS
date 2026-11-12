
import sys
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.logout_page import LogoutPage
from features.pages.login_page import LoginPage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


APP_PACKAGE = "com.tamus.pos"
APP_ACTIVITY = "com.tamus.pos.MainActivity"
DEVICE_ID = "HA2ATXGT"
WEBVIEW_CONTEXT = "WEBVIEW_com.tamus.pos"


def before_all(context):
    context.config.stdout_capture = False
    context.all_mode = context.config.userdata.get("all") == "true"
    context.logged_in = False
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = DEVICE_ID
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    options.full_reset = False
    context.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)


def switch_to_webview(context):
    for _ in range(10):
        try:
            if WEBVIEW_CONTEXT in context.driver.contexts:
                context.driver.switch_to.context(WEBVIEW_CONTEXT)
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def switch_to_native(context):
    context.driver.switch_to.context("NATIVE_APP")


def expand_menu(context):
    switch_to_native(context)
    page = LoginPage(context.driver)
    if page.exists(page.EXPAND, timeout=3):
        page.click(page.EXPAND)
        print("Menú expandido")
    else:
        print("EXPAND no disponible; se continúa")


def before_scenario(context, scenario):
    print(f"\nINICIO: {scenario.name}")
    context.driver.activate_app(APP_PACKAGE)
    time.sleep(1)
    if switch_to_webview(context):
        close_popups(context)
        if switch_to_webview(context) and LogoutPage(context.driver).find_user():
            context.logged_in = True
        else:
            context.logged_in = False
    if context.logged_in:
        expand_menu(context)
        if switch_to_webview(context):
            close_popups(context)


def close_popups(context):
    try:
        context.driver.switch_to.context(WEBVIEW_CONTEXT)
        botones = context.driver.find_elements(AppiumBy.CSS_SELECTOR, "div.tam-toast--danger button.tam-toast__close")
        for boton in botones:
            try:
                if boton.is_displayed():
                    boton.click()
                    print("Popup de aviso cerrado")
            except Exception:
                continue
        errores = context.driver.find_elements(AppiumBy.XPATH, "//*[normalize-space()='ERROR']/following::button[1]")
        for boton in errores:
            try:
                if boton.is_displayed():
                    boton.click()
                    print("Popup ERROR cerrado")
            except Exception:
                continue
    finally:
        switch_to_native(context)


def after_scenario(context, scenario):
    try:
        if switch_to_webview(context):
            close_popups(context)
    except Exception:
        pass
    finally:
        switch_to_native(context)


def after_all(context):
    if not hasattr(context, "driver") or not context.driver:
        return
    try:
        # if context.all_mode and context.logged_in:
        #     LogoutPage(context.driver).logout()
        #     context.logged_in = False
        pass
    finally:
        try:
            switch_to_native(context)
            context.driver.terminate_app(APP_PACKAGE)
        except Exception:
            pass
        try:
            context.driver.quit()
        except Exception:
            pass
