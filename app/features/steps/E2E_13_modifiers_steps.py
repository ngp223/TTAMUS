from behave import then, when
from features.pages.E2E_13_modifiers_page import ModifiersPage


@when('accedo a los modificadores')
def access_modifiers(context):
    context.modifiers = ModifiersPage(context.driver)
    context.modifiers.access_modifiers()


@then('creo un modificador')
def create_modifiers(context):
    context.modifiers.create_modifier()


@then('el modificador aparece listado')
def created_modifier(context):
    context.modifiers.check_modifier_created()


@then('modifico el modificador')
def modify_modifier(context):
    context.modifiers.modify_modifier()


@then('el modificador modificado aparece listado')
def modified_modifier(context):
    context.modifiers.check_modifier_modified()


@then('elimino el modificador')
def delete_modifier(context):
    context.modifiers.delete_modifier()
