
from behave import when, then
from features.pages.E2E_18_users_page import UsersPage


@when("accedo a usuarios")
def access_users(context):
    context.users_page = UsersPage(context.driver)
    context.users_page.access_users()


@then("creo un nuevo usuario")
def create_user(context):
    context.users_page.create_user()


@then("el usuario aparece en el listado")
def check_user_created(context):
    context.users_page.check_user_created()


@then("modifico el usuario")
def modify_user(context):
    context.users_page.modify_user()


@then("el usuario modificado aparece en el listado")
def check_user_modified(context):
    context.users_page.check_user_modified()


@then("desactivo el usuario")
def delete_user(context):
    context.users_page.deactivate_user()


@then("el usuario no aparece en el listado")
def check_user_deleted(context):
    context.users_page.check_user_deactivated()
