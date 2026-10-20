from behave import then
from features.pages.E2E_21_backups_page import BackupsPage


@then('accedo a copia de seguridad')
def access_backup(context):
    context.backups_page = BackupsPage(context.driver)
    context.backups_page.access_backup()


@then('creo la copia de respaldo')
def download_backup(context):
    context.backups_page.download_backup()


@then('la copia es listada')
def verify_backup(context):
    result = context.backups_page.verify_backup()
    assert result, "No se encontró la copia de seguridad lista"
