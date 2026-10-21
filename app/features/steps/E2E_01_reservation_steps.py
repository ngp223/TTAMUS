from behave import when, then
from features.pages.E2E_01_reservation_page import ReservationPage


@when("accedo a vista de mesas")
def access_see_tables(context):
    context.reservation_page = ReservationPage(context.driver)
    context.reservation_page.access_see_tables()


@when("selecciono la mesa")
def select_table(context):
    context.reservation_page.select_table()


@when("selecciono comensales")
def select_guests(context):
    context.reservation_page.select_guests()


@when("selecciono el producto")
def select_product(context):
    context.reservation_page.select_product()


@when("aumento la cantidad del producto")
def increase_product(context):
    context.reservation_page.increase_product()


@then("realizo el pago")
def click_pay(context):
    context.reservation_page.click_pay()
    context.reservation_page.click_verify_pay()
