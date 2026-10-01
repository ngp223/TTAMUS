from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage

class LogoutPage(BasePage):
    USER_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("[A-Z]{1,2}")')
    EXIT_POS_MODE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir del modo TPV")')
    CHANGE_USER_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cambiar usuario")')
    BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Atrás")')
    CLOSE_COMPANY_SESSION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cerrar sesión de empresa")')
    SALIR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')

    def __init__(self, driver):
        super().__init__(driver)

    def logout(self):
        self.click(self.USER_MENU)
        self.esperar_visible(self.SALIR, timeout=15)
        self.click(self.SALIR)

    def logout_if_exists(self):
        if self.existe(self.USER_MENU):
            self.logout()
            return True
        return False

    def exit_pos_mode(self):
        if self.existe(self.EXIT_POS_MODE):
            self.click(self.EXIT_POS_MODE)
            return True
        return False

    def open_change_user(self):
        if self.existe(self.CHANGE_USER_BUTTON):
            self.click(self.CHANGE_USER_BUTTON)
            return True
        return False

    def go_back(self):
        if self.existe(self.BACK_BUTTON):
            self.click(self.BACK_BUTTON)
            return True
        return False

    def close_company_session(self):
        if self.existe(self.CLOSE_COMPANY_SESSION):
            self.click(self.CLOSE_COMPANY_SESSION)
            return True
        return False