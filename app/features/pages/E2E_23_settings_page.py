import random
from features.pages.base_page import BasePage


class SettingsPage(BasePage):
    SETTINGS = BasePage.by_text_contains("Ajustes")
    GENERAL = BasePage.by_text_contains("General")
    BACK = BasePage.by_text_contains("Volver")
    APPEARANCE = BasePage.by_text_contains("Apariencia")
    ACCESSIBILITY = BasePage.by_text_contains("Accesibilidad")
    NOTIFICATIONS = BasePage.by_text_contains("Notificaciones")
    TAXES = BasePage.by_text_contains("Impuestos")
    BUSINESS = BasePage.by_text_contains("Negocio")
    ACCOUNT = BasePage.by_text_contains("Cuenta")
    TICKET_CUSTOMIZATION = BasePage.by_text("Personalización del ticket")
    TEMPLATES = [BasePage.by_id("ticket-custom-template-standard"), BasePage.by_id("ticket-custom-template-minimalist"), BasePage.by_id("ticket-custom-template-complete")]
    TEMPLATE_SAVED = BasePage.by_text("Guardado")
    APPEARANCE_OPTIONS = [["Claro", "Oscuro", "Sistema"], ["Inter", "Roboto", "IBM Plex Sans", "Manrope"], ["Discreto", "Medio", "Amplio"], ["Suave", "Neón"]]
    SCALE_INCREASE = BasePage.by_id("settings-scale-increase")
    SCALE_DECREASE = BasePage.by_id("settings-scale-decrease")
    SCALE_RESET = BasePage.by_id("settings-scale-reset")
    SCALE_VALUE = BasePage.by_id("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-ajustes-page-1-div-settings-layout-1-section-settings-content-1-div-settings-rows-1-div-settings-row-1-div-settings-row__control-1-div-scale-1-output-scale__value-1")

    def access_settings(self):
        self.scroll_text_any("Ajustes")
        self.click(self.SETTINGS)

    def general(self):
        self.click(self.GENERAL)
        self.click(self.TICKET_CUSTOMIZATION)
        self.wait_visibility(self.TEMPLATES[0])
        selected = next((t for t in self.TEMPLATES if "check_circle" in self.driver.find_element(*t).text), None)
        assert selected, "No se ha encontrado la plantilla seleccionada"
        target = next(t for t in self.TEMPLATES if t != selected)
        self.click(target)
        self.wait_text(target, "check_circle", 20)
        self.wait_visibility(self.TEMPLATE_SAVED, timeout=20)
        self.click(self.BACK)

    def appearance(self):
        self.click(self.APPEARANCE)
        for group in self.APPEARANCE_OPTIONS:
            self.click(self.by_text(random.choice(group)))

    def accessibility(self):
        self.click(self.ACCESSIBILITY)
        self.click(random.choice([self.SCALE_INCREASE, self.SCALE_DECREASE]))
        assert self.driver.find_element(*self.SCALE_VALUE).text != "100%", "El zoom no ha cambiado"
        self.click(self.SCALE_RESET)

    def notifications(self):
        self.click(self.NOTIFICATIONS)

    def taxes(self):
        self.click(self.TAXES)

    def business(self):
        self.click(self.BUSINESS)

    def account(self):
        self.click(self.ACCOUNT)