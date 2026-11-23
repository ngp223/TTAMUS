from behave import then,when
from features.pages.E2E_23_settings_page import SettingsPage


@when('accedo a copia de seguridad')
def access_settings(context):
    context.settings_page = SettingsPage(context.driver)
    context.settings_page.access_settings()


