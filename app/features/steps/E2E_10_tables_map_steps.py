from behave import when, then
from features.pages.E2E_10_tables_map_page import TablesMapPage

@when('accedo al modulo de mapa de mesas')
def access_tables_map(context):
    context.tables_map_page = TablesMapPage(context.driver)
    context.tables_map_page.tables_map()

@then('creo una nueva zona')
def create_zone(context):
    context.tables_map_page.create_zone()

@then('creo una nueva mesa')
def create_table(context):
    context.tables_map_page.create_table()

@then('modifico la zona')
def modify_zone(context):
    context.tables_map_page.modify_zone()

@then('modifico la mesa')
def modify_table(context):
    context.tables_map_page.modify_table()

@then('borro la mesa')
def delete_table(context):
    context.tables_map_page.delete_table()

@then('borro la zona')
def delete_zone(context):
    context.tables_map_page.delete_zone()
