from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def logout(self, user_initial):
        inicial = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{user_initial}")')
        salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')
        self.wait.until(EC.element_to_be_clickable(inicial)).click()
        self.wait.until(EC.element_to_be_clickable(salir)).click()
