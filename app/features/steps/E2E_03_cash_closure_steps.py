from behave import when, then
from features.pages.E2E_03_cash_closure_page import CashClosurePage


@when("accedo al cierre de caja")
def open_cash_closure(context):
    context.cash = CashClosurePage(context.driver)
    context.cash.open_cash_closure()

@then("realizo el cierre de caja")
def finalize_closure(context):
    context.cash.complete_cash_closure(context)
