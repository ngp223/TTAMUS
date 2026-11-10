
from behave import then, when
from features.pages.E2E_modifiers_page import ModifiersPage


@when('accedo a los modificadores')
def step_impl(context):
    context.modifiers = ModifiersPage(context.driver)
    context.modifiers.access_modifiers()


@then('creo un modificador')
def step_impl(context):
    context.modifiers.create_modifier()


@then('el modificador aparece listado')
def step_impl(context):
    context.modifiers.check_modifier_created()


@then('modifico el modificador')
def step_impl(context):
    context.modifiers.modify_modifier()


@then('el modificador modificado aparece listado')
def step_impl(context):
    context.modifiers.check_modifier_modified()


@then('elimino el modificador')
def step_impl(context):
    context.modifiers.delete_modifier()
