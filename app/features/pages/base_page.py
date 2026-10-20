from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click(self, locator, timeout=15):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def write(self, locator, texto, timeout=15):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(texto)
        return element

    def value_write(self, locator, texto, timeout=15):
        element = self.wait_visibility(locator, timeout)
        element.click()
        self.driver.execute_script("mobile: type", {"text": str(texto)})
        return element

    def exists(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_visibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def scroll_text(self, texto):
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{texto}"))')