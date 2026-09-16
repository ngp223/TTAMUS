from behave import given, when, then
from features.pages.E2E_01_register_page import RegisterPage


@given("pulso crear cuenta")
def step_pulso_crear_cuenta(context):
    context.register_page = RegisterPage(context.driver)
    context.register_page.click_crear_cuenta()


@when("relleno campos obligatorios")
def step_relleno_campos_obligatorios(context):
    context.register_page.rellenar_campos_obligatorios()


@then("creo usuario")
def step_creo_usuario(context):
    context.register_page.crear_usuario()

@then("el administrador esta en el restaurante") 
def step_el_administrador_esta_en_el_restaurante(context): 
    context.register_page.comprobar_administrador_en_restaurante()
    