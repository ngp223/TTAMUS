from behave import then, when
from features.pages.E2E_15_promotions_page import PromotionsPage


@when('accedo a las promociones')
def access_promotions(context):
    context.promotions = PromotionsPage(context.driver)
    context.promotions.access_promotions()


@then('creo una promoción')
def create_promotion(context):
    context.promotions.create_promotion()


@then('la promoción aparece listada')
def created_promotion(context):
    context.promotions.check_promotion_created()


@then('modifico la promoción')
def modify_promotion(context):
    context.promotions.modify_promotion()


@then('la promoción modificada aparece listada')
def modified_promotion(context):
    context.promotions.check_promotion_modified()


@then('elimino la promoción')
def delete_promotion(context):
    context.promotions.delete_promotion()
