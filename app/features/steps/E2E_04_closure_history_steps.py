from behave import when, then
from features.pages.E2E_04_closure_history_page import ClosureHistoryPage


@when("accedo al historial de cierres")
def open_closure_history(context):
    context.closures_history = ClosureHistoryPage(context.driver)
    context.closures_history.open_closure_history()


@then("veo el cierre en el historial")
def verify_closure_history(context):
    result = context.closures_history.verify_closure_history()
    assert result, "No se encontró el cierre esperado en el historial"
