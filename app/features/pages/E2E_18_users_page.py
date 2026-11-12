import random
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import REST1_USER_PIN


class UsersPage(BasePage):
    USERS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Usuarios")')
    NEW_USER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("users-add")')
    USER_NAME = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("user-edit-name")')
    EMAIL_USER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("user-edit-email")')
    ROL_USER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("user-edit-role-span-tam-select__value-1")')
    PIN_USER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("user-edit-pin")')
    USERS_SEARCH = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("users-search")')
    CREATE_SAVE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("user-edit-save")')
    EDIT = (AppiumBy.ACCESSIBILITY_ID, "Editar")
    CONFIRM_DEACTIVATE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Desactivar")')
    TIMEOUT = 15

    def __init__(self, driver):
        super().__init__(driver)
        self.created_user = None
        self.modified_user = None
        self.created_role = None

    def access_users(self):
        self.scroll_text("Usuarios")
        self.click(self.USERS)
        self.wait_visibility(self.USERS_SEARCH)
        self.wait_clickable(self.NEW_USER)

    def select_role(self, previous_role=None):
        self.click(self.ROL_USER)
        options = []
        for i in range(5):
            locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("user-edit-role-opt-{i}")')
            if self.exists(locator, timeout=3):
                options.append(locator)
        if not options:
            raise Exception("No se han encontrado roles disponibles")
        selected = random.choice(options)
        role_name = self.driver.find_element(*selected).text.strip()
        self.click(selected)
        print(f"Rol seleccionado: {role_name}")
        return role_name

    def create_user(self):
        date = datetime.now().strftime("%d%m%H%M")
        self.created_user = f"Usuari@ QA{date}"
        email = f"USERQA{date}@qa.com"
        self.click(self.NEW_USER)
        self.write(self.USER_NAME, self.created_user)
        self.write(self.EMAIL_USER, email)
        self.write(self.PIN_USER, REST1_USER_PIN)
        self.wait_visibility(self.ROL_USER)
        self.created_role = self.driver.find_element(*self.ROL_USER).text.strip()
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.USER_NAME)

    def check_user_created(self):
        self.wait_visibility(self.USERS_SEARCH)
        self.write(self.USERS_SEARCH, self.created_user)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_user}")')
        self.wait_visibility(locator)

    def modify_user(self):
        self.wait_visibility(self.USERS_SEARCH)
        self.write(self.USERS_SEARCH, self.created_user)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.created_user}")')
        self.wait_visibility(locator)
        self.click(self.EDIT)
        self.wait_visibility(self.USER_NAME)
        self.wait_visibility(self.ROL_USER)
        self.modified_user = f"{self.created_user}_modificado_{datetime.now():%H%M}"
        self.write(self.USER_NAME, self.modified_user)
        self.created_role = self.select_role(self.created_role)
        self.click(self.CREATE_SAVE)
        self.wait_invisibility(self.USER_NAME)

    def check_user_modified(self):
        self.wait_visibility(self.USERS_SEARCH)
        self.write(self.USERS_SEARCH, self.modified_user)
        self.driver.hide_keyboard()
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_user}")')
        self.wait_visibility(locator)

    def deactivate_user(self):
        self.wait_visibility(self.USERS_SEARCH)
        self.write(self.USERS_SEARCH, self.modified_user)
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_user}")')
        self.wait_visibility(locator)
        toggle = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-toggle__label.*")')
        toggles = self.driver.find_elements(*toggle)
        if len(toggles) != 1:
            raise Exception(f"Se esperaba un interruptor para {self.modified_user}, encontrados: {len(toggles)}")
        self.click(toggle)
        self.wait_clickable(self.CONFIRM_DEACTIVATE)
        self.click(self.CONFIRM_DEACTIVATE)

    def check_user_deactivated(self):
        deactivated_user = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{self.modified_user}")')
        self.wait_invisibility(deactivated_user)
