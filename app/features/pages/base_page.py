from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, InvalidSelectorException
from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import WEBVIEW_CONTEXT


class BasePage:
    EDIT = (AppiumBy.ACCESSIBILITY_ID, "Editar")
    DELETE = (AppiumBy.ACCESSIBILITY_ID, "Eliminar")
    CONFIRM_DELETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("confirm-modal-accept")')

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def by_id(resource_id):
        return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{resource_id}")'

    @staticmethod
    def by_text(text):
        return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'

    @staticmethod
    def by_text_contains(text):
        return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")'

    def wait_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def click(self, locator, timeout=15):
        element = self.wait_clickable(locator, timeout)
        element.click()
        return element

    def open_menu(self, text):
        self.scroll_text_any(text)
        return self.click(self.by_text(text))

    def click_and_wait_gone(self, click_locator, gone_locator, timeout=15):
        self.click(click_locator, timeout)
        self.wait_invisibility(gone_locator, timeout)

    def confirm_delete(self, delete_locator, gone_locator, timeout=15):
        self.click(delete_locator, timeout)
        self.click(self.CONFIRM_DELETE, timeout)
        self.wait_invisibility(gone_locator, timeout)

    def write(self, locator, text, timeout=15):
        element = self.wait_visibility(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def search_and_find(self, search_locator, text, timeout=15, attempts=3):
        for attempt in range(attempts):
            self.write(search_locator, text, timeout)
            try:
                return self.wait_visibility(self.by_text(text), timeout=5)
            except TimeoutException:
                if attempt == attempts - 1:
                    raise

    def value_write(self, locator, text, timeout=15):
        element = self.wait_visibility(locator, timeout)
        element.click()
        self.driver.execute_script("mobile: type", {"text": str(text)})
        return element

    def write_webview(self, locator, text, timeout=15):
        try:
            self.driver.switch_to.context(WEBVIEW_CONTEXT)
            element = self.wait_visibility(locator, timeout)
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
            return self.wait_visibility(locator, timeout)
        except (TimeoutException, InvalidSelectorException) as e:
            if WEBVIEW_CONTEXT not in self.driver.contexts:
                raise e
            self.driver.switch_to.context(WEBVIEW_CONTEXT)
            return self.wait_visibility(locator, timeout)

    def wait_invisibility(self, locator, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def wait_text(self, locator, text, timeout=15):
        return WebDriverWait(self.driver, timeout).until(lambda d: text in d.find_element(*locator).text)

    def scroll_text(self, text):
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{text}"))')

    def scroll_id(self, resource_id):
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().resourceId("{resource_id}"))')

    def scroll_until_visible(self, locator, container, direction="down", percent=0.6, max_scrolls=20):
        for _ in range(max_scrolls):
            found = self.driver.find_elements(*locator)
            if found and found[0].is_displayed():
                return found[0]
            self.driver.execute_script("mobile: scrollGesture", {"elementId": self.wait_visibility(container).id, "direction": direction, "percent": percent})
        raise TimeoutException(f"No se ha podido llegar a {locator}")

    def scroll_text_any(self, text, max_swipes=15):
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass
        count = len(self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().scrollable(true)'))
        for i in range(max(count, 1)):
            ui = (f'new UiScrollable(new UiSelector().scrollable(true).instance({i}))'
                  f'.setMaxSearchSwipes({max_swipes})'
                  f'.scrollIntoView(new UiSelector().text("{text}"))')
            try:
                return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)
            except NoSuchElementException:
                continue
        raise NoSuchElementException(f'No se encontró "{text}" en ninguno de los {count} scrollables')

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