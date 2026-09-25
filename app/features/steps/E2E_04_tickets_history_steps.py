from behave import when, then
from features.pages.E2E_04_tickets_history_page import TicketsHistoryPage

@when("accedo al historial de tickets")
def step_impl(context):
    context.tickets_history = TicketsHistoryPage(context.driver)
    context.tickets_history.open_tickets_history()

@then("veo el historial de tickets")
def step_impl(context):
    result = context.tickets_history.verify_tickets_history()
    assert result, "No se encontró el ticket esperado en el historial"
