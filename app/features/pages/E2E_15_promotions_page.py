from datetime import datetime
from features.pages.base_page import BasePage


class PromotionsPage(BasePage):
    NEW_PROMOTION = BasePage.by_text("Nueva Promoción")
    PROMOTION_NAME = BasePage.by_id("promotion-edit-name")
    NEXT = BasePage.by_id("promotion-edit-next")
    PROMOTIONS_SEARCH = BasePage.by_id("promotions-search")
    CREATE_SAVE = BasePage.by_id("promotion-edit-save")

    def __init__(self, driver):
        super().__init__(driver)
        self.created_promotion = None
        self.modified_promotion = None

    def access_promotions(self):
        self.open_menu("Promociones")

    def create_promotion(self):
        self.created_promotion = f"Promoción QA{datetime.now():%d%m%H%M}"
        self.click(self.NEW_PROMOTION)
        self.write(self.PROMOTION_NAME, self.created_promotion)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click_and_wait_gone(self.CREATE_SAVE, self.PROMOTION_NAME)

    def check_promotion_created(self):
        self.search_and_find(self.PROMOTIONS_SEARCH, self.created_promotion)

    def modify_promotion(self):
        self.check_promotion_created()
        self.click(self.EDIT)
        self.created_promotion += f"_modificado_{datetime.now():%d%m%H%M}"
        self.write(self.PROMOTION_NAME, self.created_promotion)
        self.click(self.NEXT)
        self.click(self.NEXT)
        self.click_and_wait_gone(self.CREATE_SAVE, self.PROMOTION_NAME)
        self.modified_promotion = self.created_promotion

    def check_promotion_modified(self):
        self.search_and_find(self.PROMOTIONS_SEARCH, self.modified_promotion)

    def delete_promotion(self):
        self.check_promotion_modified()
        self.confirm_delete(self.DELETE, self.by_text(self.modified_promotion))