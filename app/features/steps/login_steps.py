
from behave import given
from features.pages.login_page import LoginPage


@given("estoy logueado en el POS")
def login_in(context):
    login_page = LoginPage(context.driver)
    login_page.login_in()
    context.logged_in = True
