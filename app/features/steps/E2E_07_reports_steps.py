from behave import when, then
from features.pages.E2E_07_reports_page import ReportsPage


@when("accedo al módulo de informes")
def open_reports(context):
    context.reports_page = ReportsPage(context.driver)
    context.reports_page.open_reports()


@when("accedo al informe de categorías")
def open_categories_report(context):
    context.reports_page.open_categories_report()


@then("compruebo el informe de categorías")
def verify_categories_report(context):
    context.reports_page.verify_categories_report()
