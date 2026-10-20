from behave import given, when, then
from features.pages.E2E_00_register_page import RegisterPage


@given('pulso crear cuenta')
def click_create_account(context):
    context.register_page = RegisterPage(context.driver)
    context.register_page.click_create_account()


@when('relleno campos obligatorios')
def fill_mandatory_fields(context):
    context.register_page.fill_mandatory_fields()
    context.user_initial = context.register_page.initial_admin()
    context.logged_in = True


@then('el administrador esta en el restaurante')
def verify_user(context):
    context.register_page.verify_user()
