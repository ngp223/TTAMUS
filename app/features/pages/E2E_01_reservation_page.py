
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.utils.save_load_files import save_ticket
from features.config.test_config import WAIT_TIMEOUT
from datetime import datetime
import time


class ReservationPage(BasePage):
    EXPECTED_AMOUNT = "64,50 €"
    SEE_TABLES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Vista de mesas")')
    MAIN_HALL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salón principal")')
    TABLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAL-04")')
    DINERS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("3")')
    ACCEPT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Aceptar")')
    MEATS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Carnes")')
    SELECT_MEATS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Con opciones Solomillo al foie 24,50 €")')
    SELECT_VEGETABLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Verduras a la plancha")')
    RARE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Poco hecho")')
    ADD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Añadir")')
    RICES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Arroces")')
    SELECT_RICES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Risotto de setas 15,50 €")')
    SEND_TO_KITCHEN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cocina")')
    INCREASE_PRODUCT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("＋")')
    CHARGE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cobrar 64,50 €")')
    CHARGE_BUTTON = (AppiumBy.ID, "tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-sales-view-1-tam-payment-view-fill-1-div-pay-1-tam-card-tam-card-2-div-pay__actions-1-button-tam-btn-2")

    def __init__(self, driver):
        super().__init__(driver)

    def access_see_tables(self):
        return self.wait_visibility(self.SEE_TABLES, timeout=WAIT_TIMEOUT)

    def select_table(self):
        self.click(self.SEE_TABLES)
        self.wait_visibility(self.MAIN_HALL, timeout=WAIT_TIMEOUT)
        self.click(self.MAIN_HALL)
        self.wait_visibility(self.TABLE, timeout=WAIT_TIMEOUT)
        self.click(self.TABLE)
        time.sleep(2)

    def select_guests(self):
        if self.exists(self.MEATS, timeout=3):
            print("La mesa ya tiene comensales; se omite la selección")
            return
        self.click(self.DINERS)
        self.click(self.ACCEPT)
        self.wait_visibility(self.MEATS, timeout=WAIT_TIMEOUT)

    def select_product(self):
        self.click(self.MEATS)
        self.wait_visibility(self.SELECT_MEATS, timeout=WAIT_TIMEOUT)
        self.click(self.SELECT_MEATS)
        self.wait_visibility(self.SELECT_VEGETABLE, timeout=WAIT_TIMEOUT)
        self.click(self.SELECT_VEGETABLE)
        self.wait_visibility(self.RARE, timeout=WAIT_TIMEOUT)
        self.click(self.RARE)
        self.wait_visibility(self.ADD, timeout=WAIT_TIMEOUT)
        self.click(self.ADD)
        self.wait_visibility(self.RICES, timeout=WAIT_TIMEOUT)
        self.click(self.RICES)
        self.wait_visibility(self.SELECT_RICES, timeout=WAIT_TIMEOUT)
        self.click(self.SELECT_RICES)

    def increase_product(self):
        self.click(self.INCREASE_PRODUCT)

    def check_amount(self):
        try:
            button = self.driver.find_element(*self.CHARGE_BUTTON)
        except Exception:
            buttons = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textStartsWith("Cobrar ")')
            if not buttons:
                raise AssertionError("No se encuentra el botón de cobro")
            button = buttons[0]
        amount = button.text.strip().replace("Cobrar ", "", 1).strip()
        print(f"Importe de la comanda: {amount}")
        if amount != self.EXPECTED_AMOUNT:
            raise AssertionError(f"Importe incorrecto: esperado {self.EXPECTED_AMOUNT}, encontrado {amount}. No se continúa con el cobro.")
        return amount

    def save_ticket_data(self):
        amount = self.check_amount()
        date = datetime.now().strftime("%d/%m/%Y, %H:%M")
        save_ticket(date, amount)
        print(f"Ticket guardado: fecha={date!r}, importe={amount!r}")

    def click_pay(self):
        self.check_amount()
        self.click(self.SEND_TO_KITCHEN)
        self.save_ticket_data()
        self.click(self.CHARGE)

    def click_verify_pay(self):
        self.save_ticket_data()
        self.click(self.CHARGE)
