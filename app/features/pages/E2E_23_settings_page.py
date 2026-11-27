
import random
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
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
    TEMPLATES = [
        BasePage.by_id("ticket-custom-template-standard"),
        BasePage.by_id("ticket-custom-template-minimalist"),
        BasePage.by_id("ticket-custom-template-complete")
    ]
    TEMPLATE_SAVED = BasePage.by_text("Guardado")
    APPEARANCE_OPTIONS = [
        ["Claro", "Oscuro", "Sistema"],
        ["Inter", "Roboto", "IBM Plex Sans", "Manrope"],
        ["Discreto", "Medio", "Amplio"],
        ["Suave", "Neón"]
    ]
    SCALE_INCREASE = BasePage.by_id("settings-scale-increase")
    SCALE_DECREASE = BasePage.by_id("settings-scale-decrease")
    SCALE_RESET = BasePage.by_id("settings-scale-reset")
    SCALE_VALUE = BasePage.by_id("tamus-pos-tam-layout-1-tam-shell-tam-shell-1-div-tam-shell__main-1-main-tam-shell__content-1-div-view-area-1-div-content-1-tam-ajustes-page-1-div-settings-layout-1-section-settings-content-1-div-settings-rows-1-div-settings-row-1-div-settings-row__control-1-div-scale-1-output-scale__value-1")
    NOTIFICATIONS_STATUS = BasePage.by_text_matches("(?i)sin activar|concedido")
    NOTIFICATIONS_ENABLE = BasePage.by_id("settings-notifications-enable")
    NOTIFICATIONS_ALLOW = BasePage.by_id("com.android.permissioncontroller:id/permission_allow_button")
    NOTIFICATIONS_GRANTED = BasePage.by_text("Concedido")
    TAX_DEFAULT_BTN = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceIdMatches("settings-tax-default-.*")'
    )
    BUSINESS_FOOD = BasePage.by_id("business-type-alimentacion")
    BUSINESS_HOSPITALITY = BasePage.by_id("business-type-hosteleria")
    MONDAY_OPEN = BasePage.by_id("settings-hours-1-open")
    PWD_CURRENT = BasePage.by_id("pwd-current")
    PWD_NEW = BasePage.by_id("pwd-new")
    PWD_REPEAT = BasePage.by_id("pwd-repeat")
    PWD_SAVE = BasePage.by_id("account-password-save")
    PWD_ERROR = BasePage.by_text_contains("La contraseña actual no es correcta")

    def access_settings(self):
        self.scroll_text_any("Ajustes")
        self.click(self.SETTINGS)

    def general(self):
        self.click(self.GENERAL)
        self.click(self.TICKET_CUSTOMIZATION)
        self.wait_visibility(self.TEMPLATES[0])
        selected = next(
            (template for template in self.TEMPLATES
             if "check_circle" in self.driver.find_element(*template).text),
            None
        )
        assert selected, "No se ha encontrado la plantilla seleccionada"
        target = next(template for template in self.TEMPLATES if template != selected)
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
        self.wait_text(self.SCALE_VALUE, "100%")

    def notifications(self):
        status = None
        for attempt in range(3):
            self.click(self.NOTIFICATIONS)
            try:
                status = self.wait_visibility(self.NOTIFICATIONS_STATUS, 5)
                break
            except TimeoutException:
                if attempt == 2:
                    raise
        if status.text.strip().lower() == "sin activar":
            self.click(self.NOTIFICATIONS_ENABLE)
            self.click(self.NOTIFICATIONS_ALLOW)
        self.wait_text(self.NOTIFICATIONS_GRANTED, "Concedido", 15)

    def taxes(self):
        self.click(self.TAXES)
        button = self.wait_visibility(self.TAX_DEFAULT_BTN)
        tax_id = button.get_attribute("resource-id")
        self.click(self.by_id(tax_id))
        self.wait_invisibility(self.by_id(tax_id))
        restore = self.wait_visibility(self.TAX_DEFAULT_BTN)
        restore_id = restore.get_attribute("resource-id")
        self.click(self.by_id(restore_id))
        self.wait_invisibility(self.by_id(restore_id))

    def business(self):
        self.click(self.BUSINESS)
        for locator in (self.BUSINESS_FOOD,self.MONDAY_OPEN,self.MONDAY_OPEN,self.BUSINESS_HOSPITALITY):
            self.click(locator)

    def account(self):
        self.click(self.ACCOUNT)
        for field, value in ((self.PWD_CURRENT, "aaaabbbb"),(self.PWD_NEW, "bbbbaaaa"),(self.PWD_REPEAT, "bbbbaaaa")):
            element = self.wait_visibility(field)
            element.click()
            element.clear()
            element.send_keys(value)
            self.driver.hide_keyboard()
        self.click(self.PWD_SAVE, timeout=20)
        self.wait_visibility(self.PWD_ERROR, timeout=15)
