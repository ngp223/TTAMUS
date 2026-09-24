from behave import when, then
from features.pages.E2E_01_reservation_page import ReservationPage
from features.pages.E2E_00_logout_page import LogoutPage


def reservation_page(context):
    return ReservationPage(context.driver)


@when("estoy en vista de mesas")
def step_estoy_en_vista_de_mesas(context):
    reservation_page(context).comprobar_vista_mesas()


@when("selecciono la mesa")
def step_impl(context):
    reservation_page(context).select_table()


@when("selecciono comensales")
def step_impl(context):
    reservation_page(context).select_guests()
    reservation_page(context).click_accept_guests()


@when("selecciono el producto")
def step_impl(context):
    reservation_page(context).select_product_arroz_bogavante()


@when("aumento la cantidad del producto")
def step_impl(context):
    reservation_page(context).increase_product()


@then("realizo el pago")
def step_impl(context):
    reservation_page(context).click_realizar_pago()
    reservation_page(context).click_confirmar_pago()


