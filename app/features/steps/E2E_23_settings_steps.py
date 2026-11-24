from behave import then, when
from features.pages.E2E_23_settings_page import SettingsPage


@when("accedo a los ajustes")
def access_settings(context):
    context.settings_page = SettingsPage(context.driver)
    context.settings_page.access_settings()


@then("defino ajustes generales")
def define_general(context):
    context.settings_page.general()


@then("defino la apariencia")
def define_appearance(context):
    context.settings_page.appearance()


@then("defino la accesibilidad")
def define_accessibility(context):
    context.settings_page.accessibility()


@then("defino notificaciones")
def define_notifications(context):
    context.settings_page.notifications()


@then("defino impuestos")
def define_taxes(context):
    context.settings_page.taxes()


@then("defino negocio")
def define_business(context):
    context.settings_page.business()


@then("defino cuenta")
def define_account(context):
    context.settings_page.account()