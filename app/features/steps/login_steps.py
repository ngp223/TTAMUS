from behave import given
from features.pages.login_page import LoginPage


@given('estoy logueado en el POS')
def login_in(context):
    if not context.logged_in:
        LoginPage(context.driver).login_in()
        context.logged_in = True