from appium.webdriver.common.appiumby import AppiumBy
import time


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_usuario = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("A")')
        self.salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')

    def logout(self):
        self.driver.find_element(*self.menu_usuario).click()
        time.sleep(2)
        self.driver.find_element(*self.salir).click()
