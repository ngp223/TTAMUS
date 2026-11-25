from datetime import datetime
from features.pages.base_page import BasePage


class ModifiersPage(BasePage):
    NEW_GROUP = BasePage.by_text("Nuevo Grupo")
    MODIFIER_NAME = BasePage.by_id("modifier-group-name")
    SAVE_GROUP = BasePage.by_id("modifier-group-save")
    MODIFIERS_SEARCH = BasePage.by_id("modifiers-search")

    def __init__(self, driver):
        super().__init__(driver)
        self.created_modifier = None
        self.modified_modifier = None

    def access_modifiers(self):
        self.open_menu("Modificadores")

    def create_modifier(self):
        self.created_modifier = f"ModificadorQA{datetime.now():%d%m%Y%H%M%S}"
        self.click(self.NEW_GROUP)
        self.write(self.MODIFIER_NAME, self.created_modifier)
        self.driver.hide_keyboard()
        self.click_and_wait_gone(self.SAVE_GROUP, self.MODIFIER_NAME)

    def check_modifier_created(self):
        self.search_and_find(self.MODIFIERS_SEARCH, self.created_modifier)

    def modify_modifier(self):
        self.check_modifier_created()
        self.click(self.EDIT)
        self.created_modifier += f"_modificado_{datetime.now():%d%m%Y%H%M%S}"
        self.write(self.MODIFIER_NAME, self.created_modifier)
        self.click_and_wait_gone(self.SAVE_GROUP, self.MODIFIER_NAME)
        self.modified_modifier = self.created_modifier

    def check_modifier_modified(self):
        self.search_and_find(self.MODIFIERS_SEARCH, self.modified_modifier)

    def delete_modifier(self):
        self.check_modifier_modified()
        self.confirm_delete(self.DELETE, self.by_text(self.modified_modifier))