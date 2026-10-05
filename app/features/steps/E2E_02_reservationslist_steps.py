from behave import when, then
from features.pages.E2E_02_reservationslist_page import ReservationPage

@when('accedo a Reservas')
def step_accedo_a_reservas(context):
    if not hasattr(context, "reservation_page") or context.reservation_page is None:
        context.reservation_page = ReservationPage(context.driver)
    context.reservation_page.acceder_reservas()

@when('creo una nueva reserva')
def step_creo_una_nueva_reserva(context):
    context.reservation_page.crear_reserva()

@then('veo la reserva creada')
def step_veo_la_reserva_creada(context):
    context.reservation_page.comprobar_reserva_creada()