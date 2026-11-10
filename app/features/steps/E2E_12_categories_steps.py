from behave import then, when
from features.pages.E2E_12_categories_page import CategoriesPage


@when('accedo a las categorías')
def step_impl(context):
    context.categories = CategoriesPage(context.driver)
    context.categories.access_categories()


@then('creo una categoría')
def step_impl(context):
    context.categories.create_category()


@then('la categoría aparece listada')
def step_impl(context):
    context.categories.check_category_created()


@then('modifico la categoría creada')
def step_impl(context):
    context.categories.modify_category()


@then('la categoría modificada aparece listada')
def step_impl(context):
    context.categories.check_category_modified()


@then('elimino esa categoría')
def step_impl(context):
    context.categories.delete_category()