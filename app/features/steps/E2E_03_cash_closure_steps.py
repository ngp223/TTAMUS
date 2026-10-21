from behave import when, then
from features.pages.E2E_03_cash_closure_page import CashClosurePage


@when("accedo al cierre de caja")
def open_cash_closure(context):
    context.cash = CashClosurePage(context.driver)
    context.cash.open_cash_closure()


@when("abro normal declarado")
def open_declared_section(context):
    context.cash.open_declared_section()


@when("copio el esperado primero")
def copy_expected_first(context):
    context.cash.copy_expected_first()


@when("copio el esperado segundo")
def copy_expected_second(context):
    context.cash.copy_expected_second()


@when("hago scroll hasta finalizar cierre")
def scroll_to_finalize(context):
    context.cash.scroll_to_finalize()


@then("realizo el cierre de caja")
def finalize_closure(context):
    context.cash.complete_cash_closure(context)
