
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD, WAIT_TIMEOUT
from features.pages.base_page import BasePage
import time


class RegisterPage(BasePage):
    CLICK_CREATE_ACCOUNT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-auth-page-auth-page--activation-1-div-auth-layout-1-div-auth-1-p-auth-switch-1-button-auth-switch__link-1")')
    USER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    EMAIL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-4")')
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-5")')
    REPEAT_PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-6")')
    BUSINESS_TYPE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-auth-page-1-div-auth-layout-1-div-auth-1-tam-card-tam-card-1-div-auth-card__body-1-div-reg-business-1-tam-business-type-picker-1-div-biz-1-button-biz__item-1")')
    NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-7")')
    TAX_TERRITORY_DROPDOWN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1-span-tam-select__value-1")')
    TAX_TERRITORY_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-select-1-opt-0")')
    CONTINUE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continuar")')
    LEGAL_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-10")')
    PLAN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tamus-pos-tam-auth-page-1-div-auth-layout-1-div-auth-1-tam-card-tam-card-1-div-auth-card__body-1-div-plan-grid-1-button-plan-card-2")')
    ADMIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-16")')
    EMAIL_ADMIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-17")')
    PIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-18")')
    CREATE_ACCOUNT_LOGIN = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Crear cuenta y entrar")')
    SALES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("VENTAS")')

    def __init__(self, driver):
        super().__init__(driver)
        self.create_user = None
        self.create_email = None
        self.password_create = None
        self.create_admin = None
        self.initial_admin = None

    def click_create_account(self):
        self.click(self.CLICK_CREATE_ACCOUNT)

    def fill_mandatory_fields(self):
        password = TEST_PASSWORD
        hour_date = datetime.now().strftime('%d%m%Y%H%M%S')
        user = f"UsuarioQA_{hour_date}"
        email = f"{user}@sharklasers.com"
        comercial_name = f"NombreComercialQA_{hour_date}"
        legal_name = f"RazonSocialQA_{hour_date}"
        admin = f"AdministradorQA_{hour_date}"
        email_admin = f"{admin}@sharklasers.com"
        self.create_user = user
        self.create_email = email
        self.password_create = password
        self.create_admin = admin
        self.initial_admin = admin[0]
        self.write(self.USER, comercial_name)
        self.write(self.EMAIL, email)
        self.write(self.PASSWORD, password)
        self.write(self.REPEAT_PASSWORD, password)
        self.click(self.BUSINESS_TYPE)
        self.click(self.CONTINUE)
        self.write(self.NAME, comercial_name)
        self.click(self.TAX_TERRITORY_DROPDOWN)
        self.click(self.TAX_TERRITORY_OPTION)
        self.click(self.CONTINUE)
        self.write(self.LEGAL_NAME, legal_name)
        self.click(self.CONTINUE)
        self.click(self.PLAN)
        self.click(self.CONTINUE)
        self.write(self.ADMIN, admin)
        self.write(self.EMAIL_ADMIN, email_admin)
        self.write(self.PIN, "DemoQA1234")
        self.click(self.CREATE_ACCOUNT_LOGIN)
        time.sleep(2)

    def verify_user(self):
        self.wait_visibility(self.SALES, timeout=WAIT_TIMEOUT)
