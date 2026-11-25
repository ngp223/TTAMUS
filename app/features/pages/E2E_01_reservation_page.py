from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from features.pages.base_page import BasePage
from features.utils.save_load_files import save_ticket
from features.config.test_config import (
    WAIT_TIMEOUT, ORDER_HALL, ORDER_TABLE, ORDER_DINERS, ORDER_MEAT_CATEGORY, ORDER_MEAT_PRODUCT,
    ORDER_MEAT_SIDE, ORDER_MEAT_COOKING, ORDER_RICE_CATEGORY, ORDER_RICE_PRODUCT, ORDER_AMOUNTS)
from datetime import datetime


class ReservationPage(BasePage):
    EXPECTED_AMOUNT = ORDER_AMOUNTS[-1]
    CHECK_AMOUNTS = ORDER_AMOUNTS
    SEE_TABLES = BasePage.by_text("Vista de mesas")
    MAIN_HALL = BasePage.by_text(ORDER_HALL)
    TABLE = BasePage.by_text(ORDER_TABLE)
    DINERS = BasePage.by_text(ORDER_DINERS)
    ACCEPT = BasePage.by_text("Aceptar")
    MEATS = BasePage.by_text(ORDER_MEAT_CATEGORY)
    SELECT_MEATS = BasePage.by_text(ORDER_MEAT_PRODUCT)
    SELECT_VEGETABLE = BasePage.by_text(ORDER_MEAT_SIDE)
    RARE = BasePage.by_text(ORDER_MEAT_COOKING)
    ADD = BasePage.by_text("Añadir")
    RICE = BasePage.by_text(ORDER_RICE_CATEGORY)
    SELECT_RICE = BasePage.by_text(ORDER_RICE_PRODUCT)
    SEND_TO_KITCHEN = BasePage.by_text("Cocina")
    INCREASE_PRODUCT = BasePage.by_text("＋")
    CHARGE = BasePage.by_text(f"Cobrar {EXPECTED_AMOUNT}")
    CHARGE_BUTTON = (AppiumBy.ID, "tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-sales-view-1-tam-payment-view-fill-1-div-pay-1-tam-card-tam-card-2-div-pay__actions-1-button-tam-btn-2")

    def access_see_tables(self):
        return self.wait_visibility(self.SEE_TABLES, timeout=WAIT_TIMEOUT)

    def select_table(self):
        self.click(self.SEE_TABLES)
        self.click(self.MAIN_HALL, WAIT_TIMEOUT)
        self.click(self.TABLE, WAIT_TIMEOUT)
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(lambda d: d.find_elements(*self.ACCEPT) or d.find_elements(*self.MEATS))

    def select_guests(self):
        if self.exists(self.MEATS, timeout=3):
            print("La mesa ya tiene comensales; se omite la selección")
            return
        self.click(self.DINERS)
        self.click(self.ACCEPT)
        self.wait_visibility(self.MEATS, timeout=WAIT_TIMEOUT)

    def select_product(self):
        self.click(self.MEATS)
        self.click(self.SELECT_MEATS, WAIT_TIMEOUT)
        self.click(self.SELECT_VEGETABLE, WAIT_TIMEOUT)
        self.click(self.RARE, WAIT_TIMEOUT)
        self.click(self.ADD, WAIT_TIMEOUT)
        self.check_amount(self.CHECK_AMOUNTS[0])
        self.click(self.RICE, WAIT_TIMEOUT)
        self.click(self.SELECT_RICE, WAIT_TIMEOUT)
        self.check_amount(self.CHECK_AMOUNTS[1])

    def increase_product(self):
        self.click(self.INCREASE_PRODUCT)
        self.check_amount(self.CHECK_AMOUNTS[2])

    def check_amount(self, expected):
        amount = ""

        def amount_matches(driver):
            nonlocal amount
            buttons = driver.find_elements(*self.CHARGE_BUTTON) or driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textStartsWith("Cobrar ")')
            if buttons and buttons[0].is_displayed():
                amount = buttons[0].text.strip().replace("Cobrar ", "", 1).strip()
                return amount == expected
            return False

        try:
            WebDriverWait(self.driver, 5, poll_frequency=0.5, ignored_exceptions=(StaleElementReferenceException,)).until(amount_matches)
        except TimeoutException:
            raise AssertionError(f"Importe incorrecto: esperado {expected}, encontrado {amount}. No se continúa.") from None
        print(f"Importe correcto: {amount}")
        return amount

    def save_ticket_data(self):
        amount = self.check_amount(self.EXPECTED_AMOUNT)
        date = datetime.now().strftime("%d/%m/%Y, %H:%M")
        save_ticket(date, amount)
        print(f"Ticket guardado: fecha={date!r}, importe={amount!r}")

    def click_pay(self):
        self.click(self.SEND_TO_KITCHEN)
        self.click_verify_pay()

    def click_verify_pay(self):
        self.save_ticket_data()
        self.click(self.CHARGE)