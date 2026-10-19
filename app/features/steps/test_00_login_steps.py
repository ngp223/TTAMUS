from behave import given
from features.pages.login_page import LoginPage


@given("estoy logueado en el POS")
def login_in(context):
    LoginPage(context.driver).login()
    context.logged_in = True
