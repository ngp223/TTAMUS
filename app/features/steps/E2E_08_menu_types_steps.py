from behave import when, then
from features.pages.E2E_08_menu_types_page import CardsPage


@when("accedo al módulo de cartas")
def open_cards(context):
    context.cards_page = CardsPage(context.driver)
    context.cards_page.open_cards()


@then("creo una nueva carta con datos válidos")
def create_new_card(context):
    context.cards_page.create_new_card()


@then("modifico la carta creada")
def modify_created_card(context):
    context.cards_page.modify_created_card()


@then("compruebo que la modificación se ha hecho")
def verify_modification(context):
    context.cards_page.verify_modification()


@then("borro la carta creada")
def delete_created_card(context):
    context.cards_page.delete_created_card()
