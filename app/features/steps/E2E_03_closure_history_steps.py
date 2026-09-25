from behave import when, then
from features.pages.E2E_03_closure_history_page import ClosureHistoryPage


@when("accedo al historial de cierres")
def step_impl(context):
    context.closures_history = ClosureHistoryPage(context.driver)
    context.closures_history.open_closure_history()


@then("veo el cierre en el historial")
def step_impl(context):
    result = context.closures_history.verify_closure_history()
    assert result, "No se encontró el cierre esperado en el historial"
