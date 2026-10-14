from behave import when, then
from features.pages.E2E_09_menus_page import MenusPage

@when('accedo al módulo de menus')
def step_accedo_modulo_menus(context):
    if not hasattr(context, "menus_page") or context.menus_page is None:
        context.menus_page = MenusPage(context.driver)
    context.menus_page.acceder_menus()

@then('creo un nuevo menu con datos válidos')
def step_creo_nuevo_menu(context):
    context.menus_page.crear_menu()

@then('modifico el menu')
def step_modifico_menu(context):
    context.menus_page.modificar_menu()

@then('compruebo el menu modificado')
def step_compruebo_menu_modificado(context):
    context.menus_page.comprobar_menu_modificado()

@then('borro el menu')
def step_borro_menu(context):
    context.menus_page.borrar_menu()