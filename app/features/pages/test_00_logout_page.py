from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage

class LogoutPage(BasePage):
    EXIT_POS_MODE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir del modo TPV")')
    CHANGE_USER_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cambiar usuario")')
    BACK_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Atrás")')
    CLOSE_COMPANY_SESSION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cerrar sesión de empresa")')

    def __init__(self, driver):
        super().__init__(driver)

    def logout(self, user_initial):
        inicial = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{user_initial}")')
        salir = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Salir")')
        self.click(inicial)
        self.click(salir)

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
