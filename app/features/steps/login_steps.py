from behave import given
from features.pages.login_page import LoginPage

@given('estoy logueado en el POS')
def login_in(context):
    if not getattr(context, "logged_in", False):
        LoginPage(context.driver).login_in(context)

