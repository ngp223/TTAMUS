from appium.webdriver.common.appiumby import AppiumBy
from features.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
import random


class SettingsPage(BasePage):
    SETTINGS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Ajustes")')
    GENERAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("General")')
    BACK = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Volver")')
    APPEARANCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Apariencia")')
    ACCESSIBILITY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Accesibilidad")')
    NOTIFICATIONS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Notificaciones")')
    TAXES = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Impuestos")')
    BUSINESS = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Negocio")')
    ACCOUNT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Cuenta")')
    TICKET_CUSTOMIZATION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Personalización del ticket")')
    TEMPLATE_STANDARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("ticket-custom-template-standard")')
    TEMPLATE_MINIMALIST = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("ticket-custom-template-minimalist")')
    TEMPLATE_COMPLETE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("ticket-custom-template-complete")')
    TEMPLATE_SAVED = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Guardado")')
    TEMPLATE_UNSAVED = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cambios sin guardar")')
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
        templates = [self.TEMPLATE_STANDARD, self.TEMPLATE_MINIMALIST, self.TEMPLATE_COMPLETE]
        self.wait_visibility(self.TEMPLATE_STANDARD, timeout=15)
        selected = None
        for template in templates:
            if "check_circle" in self.driver.find_element(*template).text:
                selected = template
                break
        if selected is None:
            raise AssertionError("No se ha encontrado la plantilla seleccionada")
        target = next(template for template in templates if template != selected)
        self.click(target)
        self.wait_visibility(self.TEMPLATE_UNSAVED, timeout=10)
        WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element(*self.TEMPLATE_SAVED).is_displayed())
        WebDriverWait(self.driver, 20).until(lambda driver: "check_circle" in driver.find_element(*target).text)
        print("Plantilla de ticket cambiada y guardada correctamente")
        self.click(self.BACK)

    def appearance(self):
        self.click(self.APPEARANCE)
        opciones = [["Claro", "Oscuro", "Sistema"], ["Inter", "Roboto", "IBM Plex Sans", "Manrope"],
                    ["Discreto", "Medio", "Amplio"], ["Suave", "Neón"]]
        for grupo in opciones:
            opcion = random.choice(grupo)
            self.click((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{opcion}")'))

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