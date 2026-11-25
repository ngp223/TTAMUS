import random
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from features.config.test_config import REST1_USER_PIN


class UsersPage(BasePage):
    NEW_USER = BasePage.by_id("users-add")
    USER_NAME = BasePage.by_id("user-edit-name")
    EMAIL_USER = BasePage.by_id("user-edit-email")
    ROL_USER = BasePage.by_id("user-edit-role-span-tam-select__value-1")
    PIN_USER = BasePage.by_id("user-edit-pin")
    USERS_SEARCH = BasePage.by_id("users-search")
    CREATE_SAVE = BasePage.by_id("user-edit-save")
    CONFIRM_DEACTIVATE = BasePage.by_text("Desactivar")
    TOGGLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceIdMatches(".*tam-toggle__label.*")')

    def __init__(self, driver):
        super().__init__(driver)
        self.created_user = None
        self.modified_user = None
        self.created_role = None

    def access_users(self):
        self.open_menu("Usuarios")
        self.wait_visibility(self.USERS_SEARCH)
        self.wait_clickable(self.NEW_USER)

    def select_role(self):
        self.click(self.ROL_USER)
        options = [self.by_id(f"user-edit-role-opt-{i}") for i in range(5) if self.exists(self.by_id(f"user-edit-role-opt-{i}"), timeout=3)]
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
        self.driver.hide_keyboard()
        self.click(self.NEW_USER)
        self.write(self.USER_NAME, self.created_user)
        self.write(self.EMAIL_USER, f"USERQA{date}@qa.com")
        self.write(self.PIN_USER, REST1_USER_PIN)
        self.created_role = self.wait_visibility(self.ROL_USER).text.strip()
        self.click_and_wait_gone(self.CREATE_SAVE, self.USER_NAME)

    def check_user_created(self):
        self.search_and_find(self.USERS_SEARCH, self.created_user)
        self.driver.hide_keyboard()

    def modify_user(self):
        self.search_and_find(self.USERS_SEARCH, self.created_user)
        self.click(self.EDIT)
        self.wait_visibility(self.USER_NAME)
        self.driver.hide_keyboard()
        self.wait_visibility(self.ROL_USER)
        self.modified_user = f"{self.created_user}_modificado_{datetime.now():%H%M}"
        self.write(self.USER_NAME, self.modified_user)
        self.created_role = self.select_role()
        self.click_and_wait_gone(self.CREATE_SAVE, self.USER_NAME)

    def check_user_modified(self):
        self.search_and_find(self.USERS_SEARCH, self.modified_user)

    def deactivate_user(self):
        self.search_and_find(self.USERS_SEARCH, self.modified_user)
        toggles = self.driver.find_elements(*self.TOGGLE)
        if len(toggles) != 1:
            raise Exception(f"Se esperaba un interruptor para {self.modified_user}, encontrados: {len(toggles)}")
        self.click(self.TOGGLE)
        self.click(self.CONFIRM_DEACTIVATE)

    def check_user_deactivated(self):
        self.wait_invisibility(self.by_text(self.modified_user))