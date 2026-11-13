from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, InvalidSelectorException
from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import WEBVIEW_CONTEXT


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def click(self, locator, timeout=15):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def write(self, locator, text, timeout=15):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return element

    def search(self, locator, text, timeout=15):
        element = self.write(locator, text, timeout)
        self.driver.hide_keyboard()
        return element

    def search_and_find(self, search_locator, text, timeout=15):
        self.search(search_locator, text, timeout)
        return self.wait_visibility((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'), timeout)

    def value_write(self, locator, text, timeout=15):
        element = self.wait_visibility(locator, timeout)
        element.click()
        self.driver.execute_script("mobile: type", {"text": str(text)})
        return element

    def write_webview(self, locator, text, timeout=15):
        try:
            self.driver.switch_to.context(WEBVIEW_CONTEXT)
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            return element
        except Exception as e:
            raise Exception(f"No se ha podido escribir en el campo {locator}: {e}")
        finally:
            self.driver.switch_to.context("NATIVE_APP")

    def exists(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_visibility(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_visibility_contexts(self, locator, timeout=15):
        try:
            self.driver.switch_to.context("NATIVE_APP")
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except (TimeoutException, InvalidSelectorException) as e:
            if WEBVIEW_CONTEXT not in self.driver.contexts:
                raise e
            self.driver.switch_to.context(WEBVIEW_CONTEXT)
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_invisibility(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def scroll_text(self, text):
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))')

    def wait_date_amount_match(self, date_locator, amount_locator, expected_date, expected_amount, timeout=15, tolerance=60):
        date_format = "%d/%m/%Y, %H:%M"
        expected = datetime.strptime(expected_date.strip(), date_format)
        found = {}

        def matches(driver):
            found["date"] = driver.find_element(*date_locator).text.strip()
            found["amount"] = driver.find_element(*amount_locator).text.strip()
            actual = datetime.strptime(found["date"], date_format)
            return found["amount"] == expected_amount.strip() and abs((actual - expected).total_seconds()) <= tolerance

        try:
            WebDriverWait(self.driver, timeout, ignored_exceptions=(NoSuchElementException, StaleElementReferenceException, ValueError)).until(matches)
            print(f"Encontrado en la primera fila: fecha={found['date']!r}, importe={found['amount']!r}")
            return True
        except TimeoutException:
            print(f"Fecha encontrada: {found.get('date')!r} | esperada: {expected_date!r}")
            print(f"Importe encontrado: {found.get('amount')!r} | esperado: {expected_amount!r}")
            return False