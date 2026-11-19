from behave import when, then
from features.pages.E2E_19_roles_page import RolesPage


@when("accedo a roles")
def access_roles(context):
    context.roles_page = RolesPage(context.driver)
    context.roles_page.access_roles()


@then("creo un nuevo rol")
def create_role(context):
    context.roles_page.create_role()


@then("el rol aparece en el listado")
def role_in_list(context):
    context.roles_page.check_role_created()


@then("modifico el rol")
def modify_role(context):
    context.roles_page.modify_role()


@then("el rol modificado aparece en el listado")
def modified_role_in_list(context):
    context.roles_page.check_role_modified()


@then("elimino el rol")
def delete_role(context):
    context.roles_page.delete_role()


@then("el rol no aparece en el listado")
def role_not_in_list(context):
    context.roles_page.check_role_deleted()