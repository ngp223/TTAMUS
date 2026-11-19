from behave import then, when
from features.pages.E2E_14_products_page import ProductsPage


@when('accedo a los productos')
def access_products(context):
    context.products = ProductsPage(context.driver)
    context.products.access_products()


@then('creo un producto')
def create_product(context):
    context.products.create_product()


@then('el producto aparece listado')
def created_product(context):
    context.products.check_product_created()


@then('modifico ese producto')
def modify_product(context):
    context.products.modify_product()


@then('el producto modificado aparece listado')
def modified_product(context):
    context.products.check_product_modified()


@then('elimino el producto')
def delete_product(context):
    context.products.delete_product()
