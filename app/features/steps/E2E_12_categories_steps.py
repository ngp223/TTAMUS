from behave import then, when
from features.pages.E2E_12_categories_page import CategoriesPage


@when('accedo a las categorías')
def access_category(context):
    context.categories = CategoriesPage(context.driver)
    context.categories.access_categories()


@then('creo una categoría')
def create_category(context):
    context.categories.create_category()


@then('la categoría aparece listada')
def created_category(context):
    context.categories.check_category_created()


@then('modifico la categoría creada')
def modify_category(context):
    context.categories.modify_category()


@then('la categoría modificada aparece listada')
def modified_category(context):
    context.categories.check_category_modified()


@then('elimino esa categoría')
def delete_category(context):
    context.categories.delete_category()