import sys
import os

from appium import webdriver
from appium.options.android import UiAutomator2Options

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

    context.driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

def after_all(context):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()
        