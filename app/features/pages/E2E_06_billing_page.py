from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time

class BillingPage(BasePage):
    INVOICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Facturación")')
    NEW_INVOICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva Factura")')
    CONCEPT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-10")')
    QUANTITY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-11")')
    PRICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-12")')
    CUSTOMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1")')
    OPTION_CUSTOMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1-opt-1")')
    CONFIRM_INVOICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirmar y Emitir Factura")')
    CONCEPT_VALUE = "ProductoQA"
    QUANTITY_VALUE = "2"
    PRICE_VALUE = "30"

    def __init__(self, driver):
        super().__init__(driver)

    def open_billing(self):
        self.click(self.INVOICE)

    def create_new_invoice(self):
        self.click(self.NEW_INVOICE)
        self.click(self.CUSTOMER)
        self.click(self.OPTION_CUSTOMER)
        self.write(self.CONCEPT, self.CONCEPT_VALUE)
        quantity = self.driver.find_element(*self.QUANTITY)
        quantity.clear()
        time.sleep(1)
        self.value_write(self.QUANTITY, self.QUANTITY_VALUE)
        self.value_write(self.PRICE, self.PRICE_VALUE)
        self.driver.hide_keyboard()
        now = datetime.now()
        self.date_invoice = f"{now.day}/{now.month}/{now.year}, {now.strftime('%H:%M')}"
        self.total_invoice = int(self.QUANTITY_VALUE) * int(self.PRICE_VALUE)
        self.click(self.CONFIRM_INVOICE)

    def invoice_appears_in_list(self):
        try:
            row_locator = (AppiumBy.XPATH, f'//*[contains(@text, "{self.date_invoice}")]/..')
            row = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(row_locator))
            row.find_element(AppiumBy.XPATH, f'.//*[contains(@text, "{self.total_invoice }")]')
            return True
        except Exception as e:
            print(f"No se encontró la factura con fecha {self.date_invoice} e importe {self.total_invoice }: {e}")
            return False