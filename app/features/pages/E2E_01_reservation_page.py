from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ReservationPage:
    VISTA_MESAS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Vista de mesas")')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def comprobar_vista_mesas(self):
        self.wait.until(EC.visibility_of_element_located(self.VISTA_MESAS))
