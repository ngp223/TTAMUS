from behave import when, then
from features.pages.test_00_login_page import LoginPage
from features.pages.test_00_logout_page import LogoutPage


@when("hago logout")
def step_hago_logout(context):
    LogoutPage(context.driver).logout(context.user_initial)
    context.logged_in = False


@then("el usuario ha cerrado sesión")
def step_usuario_ha_cerrado_sesion(context):
    assert LoginPage(context.driver).comprobar_login()
    context.logged_in = False
