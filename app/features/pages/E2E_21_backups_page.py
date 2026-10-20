from appium.webdriver.common.appiumby import AppiumBy
from features.config.test_config import TEST_PASSWORD
from features.pages.base_page import BasePage


class BackupsPage(BasePage):
    PASSWORD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("tam-input-3")')
    BACKUPS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copias de Seguridad").instance(0)')
    DOWNLOAD_BACKUP = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Descargar copia cifrada")')
    LIST_COPY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Copia lista")')

    def __init__(self, driver):
        super().__init__(driver)

    def access_backup(self):
        self.scroll_text("Copias de Seguridad")
        self.click(self.BACKUPS)

    def download_backup(self):
        self.write(self.PASSWORD, TEST_PASSWORD)
        self.click(self.DOWNLOAD_BACKUP)

    def verify_backup(self):
        return self.exists(self.LIST_COPY, timeout=15)
