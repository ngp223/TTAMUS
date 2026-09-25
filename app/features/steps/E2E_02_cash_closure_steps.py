from behave import when, then
from datetime import datetime
from features.pages.E2E_02_cash_closure_page import CashClosurePage
from features.utils.tickets_store import save_ticket

@when("accedo al cierre de caja")
def step_impl(context):
    context.cash = CashClosurePage(context.driver)
    context.cash.open_cash_closure()

@when("abro normal declarado")
def step_impl(context):
    context.cash.open_declared_section()

@when("copio el esperado primero")
def step_impl(context):
    context.cash.copy_expected_first()

@when("copio el esperado segundo")
def step_impl(context):
    context.cash.copy_expected_second()

@when("hago scroll hasta finalizar cierre")
def step_impl(context):
    context.cash.scroll_to_finalize()

@then("realizo el cierre de caja")
def step_impl(context):
    context.last_closure_date = datetime.now().strftime("%d/%m/%Y, %H:%M")
    context.last_closure_amount = context.cash.get_closure_total()
    print(f"Fecha cierre: {context.last_closure_date}")
    print(f"Importe cierre: {context.last_closure_amount}")
    context.cash.finalize_closure()
    save_ticket(context.last_closure_date, context.last_closure_amount)
    print("Ticket guardado correctamente")
