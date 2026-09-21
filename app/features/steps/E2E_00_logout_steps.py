from behave import given, when, then
from features.pages.E2E_00_logout_page import LogoutPage

@when('hago logout')
def step_hago_logout(context):
    LogoutPage(context.driver).logout(context.user_initial)
    context.logged_in = False

@then('el usuario ha cerrado sesión')
def step_usuario_ha_cerrado_sesion(context):
    context.logged_in = False
