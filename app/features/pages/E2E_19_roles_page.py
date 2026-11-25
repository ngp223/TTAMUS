import random
from datetime import datetime
from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage


class RolesPage(BasePage):
    ROLE_CREATE = BasePage.by_id("roles-create")
    ROLE_NAME = BasePage.by_id("role-edit-name")
    ROLE_SAVE = BasePage.by_id("role-edit-save")
    PERM_GROUPS = [1, 2, 3, 4, 5]
    GROUP_CHECKBOXES = '//android.view.View[contains(@resource-id,"perms__group-{}")]//android.widget.CheckBox'
    DELETE_BTN = '//*[@text="{}"]/ancestor::*[.//*[@content-desc="Eliminar"]][1]//*[@content-desc="Eliminar"]'
    DATE_FORMAT = "%d%m%H%M%S"

    def __init__(self, driver):
        super().__init__(driver)
        self.created_role = None
        self.modified_role = None

    def _check_random(self, groups, only_unchecked=False):
        ids = []
        for group in groups:
            boxes = self.driver.find_elements(AppiumBy.XPATH, self.GROUP_CHECKBOXES.format(group))
            ids += [b.get_attribute("resource-id") for b in boxes if not only_unchecked or b.get_attribute("checked") != "true"]
        if not ids:
            return None
        perm_id = random.choice(ids)
        try:
            self.scroll_id(perm_id)
        except Exception:
            pass
        self.click(self.by_id(perm_id))
        print(f"Permiso marcado: {perm_id}")
        return perm_id

    def _in_list(self, name):
        try:
            return self.wait_visibility(self.by_text(name), timeout=5)
        except Exception:
            self.scroll_text_any(name)
            return self.wait_visibility(self.by_text(name), timeout=5)

    def access_roles(self):
        self.open_menu("Roles")
        self.wait_clickable(self.ROLE_CREATE)

    def create_role(self):
        self.created_role = f"Rol QA{datetime.now():{self.DATE_FORMAT}}"
        self.click(self.ROLE_CREATE)
        self.write(self.ROLE_NAME, self.created_role)
        if not [p for p in (self._check_random([g]) for g in self.PERM_GROUPS) if p]:
            raise Exception("No se ha podido marcar ningún permiso")
        self.click_and_wait_gone(self.ROLE_SAVE, self.ROLE_NAME)

    def check_role_created(self):
        self._in_list(self.created_role)

    def modify_role(self):
        self._in_list(self.created_role).click()
        self.modified_role = f"{self.created_role}_modificado_{datetime.now():{self.DATE_FORMAT}}"
        self.write(self.ROLE_NAME, self.modified_role)
        if not self._check_random(self.PERM_GROUPS, only_unchecked=True):
            raise Exception("No quedan permisos sin marcar para añadir")
        self.click_and_wait_gone(self.ROLE_SAVE, self.ROLE_NAME)

    def check_role_modified(self):
        self._in_list(self.modified_role)
        if self.exists(self.by_text(self.created_role), timeout=2):
            raise Exception(f"Sigue apareciendo el nombre antiguo: {self.created_role}")

    def delete_role(self):
        self._in_list(self.modified_role)
        self.confirm_delete((AppiumBy.XPATH, self.DELETE_BTN.format(self.modified_role)), self.by_text(self.modified_role))

    def check_role_deleted(self):
        self.wait_invisibility(self.by_text(self.modified_role))