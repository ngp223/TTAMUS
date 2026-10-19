from behave import when, then
from features.pages.E2E_06_billing_page import BillingPage


@when("accedo al módulo de facturación")
def open_billing(context):
    context.billing_page = BillingPage(context.driver)
    context.billing_page.open_billing()


@then("creo una nueva factura con datos válidos")
def create_new_invoice(context):
    context.billing_page.create_new_invoice()


@then("la factura se crea correctamente")
def invoice_created_successfully(context):
    context.billing_page.invoice_created_successfully()


@then("veo la factura en el listado de facturas")
def invoice_appears_in_list(context):
    context.billing_page.invoice_appears_in_list()
