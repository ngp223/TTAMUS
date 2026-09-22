from behave import when
from features.pages.E2E_01_reservation_page import ReservationPage

@when("estoy en vista de mesas")
def step_estoy_en_vista_de_mesas(context):
    ReservationPage(context.driver).comprobar_vista_mesas()

