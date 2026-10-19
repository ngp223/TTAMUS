from behave import when, then
from features.pages.E2E_02_reservationslist_page import ReservationPage


@when('accedo a Reservas')
def access_reservation(context):
    context.reservation_page = ReservationPage(context.driver)
    context.reservation_page.access_reservation()


@when('creo una nueva reserva')
def create_reservation(context):
    context.reservation_page.create_reservation()


@when('veo la reserva creada')
def verify_create_reservation(context):
    context.reservation_page.verify_create_reservation()


@when('edito la reserva')
def edit_reservation(context):
    context.reservation_page.edit_reservation()


@when('marco la reserva como llegada')
def check_reservation(context):
    context.reservation_page.check_reservation()


@then('cancelo la reserva')
def cancel_reservation(context):
    context.reservation_page.cancel_reservation()


@then('no veo la reserva cancelada')
def verify_cancel_reservation(context):
    context.reservation_page.verify_cancel_reservation()
