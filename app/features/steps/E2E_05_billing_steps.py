from behave import when, then
from features.pages.E2E_05_billing_page import BillingPage


@when("accedo al módulo de facturación")
def step_impl(context):
    context.billing_page = BillingPage(context.driver)
    context.billing_page.open_billing()


@then("creo una nueva factura con datos válidos")
def step_impl(context):
    context.billing_page.create_new_invoice()


@then("la factura se crea correctamente")
def step_impl(context):
    context.billing_page.invoice_created_successfully()


@then("veo la factura en el listado de facturas")
def step_impl(context):
    context.billing_page.invoice_appears_in_list()