from behave import when, then
from features.pages.E2E_09_menus_page import MenusPage

@when('accedo al módulo de menus')
def open_menus(context):
    context.menus_page = MenusPage(context.driver)
    context.menus_page.open_menus()

@then('creo un nuevo menu con datos válidos')
def create_menu(context):
    context.menus_page.create_menu()

@then('modifico el menu')
def modify_menu(context):
    context.menus_page.modify_menu()

@then('compruebo el menu modificado')
def verify_menu_modificated(context):
    context.menus_page.verify_menu_modificated()

@then('borro el menu')
def delete_menu(context):
    context.menus_page.delete_menu()
