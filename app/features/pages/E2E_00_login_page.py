from appium.webdriver.common.appiumby import AppiumBy


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.usuario = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("PON_AQUI_EL_RESOURCE_ID")')
        self.password = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("PON_AQUI_EL_RESOURCE_ID")')
        self.entrar = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar")')

    def login(self):
        self.driver.find_element(*self.usuario).send_keys("USUARIO")
        self.driver.find_element(*self.password).send_keys("PASSWORD")
        self.driver.find_element(*self.entrar).click()
