from behave import then
from features.pages.E2E_21_backups_page import BackupsPage


@then("accedo a copia de seguridad")
def step_impl(context):
    context.backup_page = BackupsPage(context.driver)
    context.backup_page.acceder_copias_seguridad()


@then("creo la copia de respaldo")
def step_impl(context):
    context.backup_page.descargar_backup()


@then("la copia es listada")
def step_impl(context):
    assert context.backup_page.comprobar_copia_lista()
