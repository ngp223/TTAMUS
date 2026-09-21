from behave import given
from features.pages.E2E_00_login_page import LoginPage


@given("estoy logueado en el POS")
def step_estoy_logueado(context):
    LoginPage(context.driver).login()
    context.logged_in = True
