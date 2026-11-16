from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from features.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import random


class BillingPage(BasePage):
    INVOICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Facturación")')
    NEW_INVOICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Nueva Factura")')
    CONCEPT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("invoice-new-line-concept-draft-line-1")')
    QUANTITY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("invoice-new-line-quantity-draft-line-1")')
    PRICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("invoice-new-line-price-draft-line-1")')
    CUSTOMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("invoice-new-saved-customer")')
    OPTION_CUSTOMER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("invoice-new-saved-customer-opt-2")')
    CONFIRM_INVOICE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirmar y Emitir Factura")')
    CONCEPT_VALUE = "ProductoQA"
    QUANTITY_VALUE = str(random.randint(1, 50))
    PRICE_VALUE = str(random.randint(10, 100))

    def __init__(self, driver):
        super().__init__(driver)
        self.total_invoice = None
        self.date_invoice = None
        self.date_invoice_end = None

    def open_billing(self):
        self.click(self.INVOICE)

    def create_new_invoice(self):
        self.click(self.NEW_INVOICE)
        self.click(self.CUSTOMER)
        self.click(self.OPTION_CUSTOMER)
        self.write(self.CONCEPT, self.CONCEPT_VALUE)
        self.wait_visibility(self.QUANTITY).clear()
        time.sleep(1)
        self.value_write(self.QUANTITY, self.QUANTITY_VALUE)
        self.value_write(self.PRICE, self.PRICE_VALUE)
        self.driver.hide_keyboard()
        now = datetime.now()
        self.date_invoice = f"{now.day}/{now.month}/{now.year}, {now.hour}:{now.minute:02d}"
        self.total_invoice = int(self.QUANTITY_VALUE) * int(self.PRICE_VALUE)
        self.click(self.CONFIRM_INVOICE)
        end = datetime.now()
        self.date_invoice_end = f"{end.day}/{end.month}/{end.year}, {end.hour}:{end.minute:02d}"

    def invoice_appears_in_list(self):
        price = ""
        try:
            price = f"{self.total_invoice:,}".replace(",", ".")
            row_locator = (AppiumBy.XPATH, f'//*[contains(@text, "{self.date_invoice}") or contains(@text, "{self.date_invoice_end}")]/..')
            invoice = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(row_locator))
            price_locator = (AppiumBy.XPATH, f'.//*[contains(@text, "{price}")]')
            WebDriverWait(self.driver, 10).until(lambda d: invoice.find_elements(*price_locator))
            print(f"Encontró la factura con fecha {self.date_invoice} e importe {price},00 €")
            return True
        except Exception as e:
            raise AssertionError(f"No se encontró la factura con fecha {self.date_invoice} (o {self.date_invoice_end}) e importe {price}: {e}")