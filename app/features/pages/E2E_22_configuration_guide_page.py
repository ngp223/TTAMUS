from features.pages.base_page import BasePage


class ConfigurationGuidePage(BasePage):
    GUIDE_OPEN_WIZARD = BasePage.by_id("guide-open-wizard")
    GUIDE_WIZARD_SKIP = BasePage.by_id("guide-wizard-skip")
    GUIDE_WIZARD_START_SELLING = BasePage.by_id("guide-wizard-start-selling")
    GUIDE_WIZARD_OPEN_CERTIFICATE = BasePage.by_id("guide-wizard-open-certificate")

    def access_configurationguide(self):
        self.open_menu("Guía de configuración")

    def configure(self):
        self.click(self.GUIDE_OPEN_WIZARD)
        if not self.exists(self.GUIDE_WIZARD_SKIP):
            self.click(self.GUIDE_WIZARD_OPEN_CERTIFICATE)
        self.click(self.GUIDE_WIZARD_SKIP)
        self.click(self.GUIDE_WIZARD_START_SELLING)