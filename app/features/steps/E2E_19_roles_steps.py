from behave import step
from features.pages.E2E_19_roles_page import RolesPage


@step("accedo a roles")
def access_roles(context):
    context.roles_page = RolesPage(context.driver)
    context.roles_page.access_roles()


@step("creo un nuevo rol")
def create_role(context):
    context.roles_page.create_role()


@step("el rol aparece en el listado")
def role_in_list(context):
    context.roles_page.check_role_created()


@step("modifico el rol")
def modify_role(context):
    context.roles_page.modify_role()


@step("el rol modificado aparece en el listado")
def modified_role_in_list(context):
    context.roles_page.check_role_modified()


@step("elimino el rol")
def delete_role(context):
    context.roles_page.delete_role()


@step("el rol no aparece en el listado")
def role_not_in_list(context):
    context.roles_page.check_role_deleted()