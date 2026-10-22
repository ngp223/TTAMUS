
from behave import when, then
from features.pages.E2E_08_menu_types_page import MenuTypesPage


@when("accedo al módulo de cartas")
def open_menutypes(context):
    context.menutypes_page = MenuTypesPage(context.driver)
    context.menutypes_page.open_menutypes()


@then("creo una nueva carta con datos válidos")
def create_new_menutypes(context):
    context.menutypes_page.create_new_menutype()


@then("modifico la carta creada")
def modify_created_menutypes(context):
    context.menutypes_page.modify_created_menutypes()


@then("compruebo que la modificación se ha hecho")
def verify_modification(context):
    context.menutypes_page.verify_modification()


@then("borro la carta creada")
def delete_created_menutypes(context):
    context.menutypes_page.delete_created_menutypes()
