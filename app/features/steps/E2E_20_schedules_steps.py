from behave import step
from features.pages.E2E_20_schedules_page import SchedulesPage


@step("accedo a horarios")
def access_schedules(context):
    context.schedules_page = SchedulesPage(context.driver)
    context.schedules_page.access_schedules()


@step("creo un nuevo turno")
def create_shift(context):
    context.schedules_page.create_shift()


@step("el turno aparece en el calendario")
def shift_created(context):
    context.schedules_page.check_shift_created()


@step("modifico la hora de inicio del turno")
def modify_shift(context):
    context.schedules_page.modify_shift()


@step("la hora de inicio del turno está modificada")
def shift_modified(context):
    context.schedules_page.check_shift_modified()


@step("elimino el turno")
def delete_shift(context):
    context.schedules_page.delete_shift()


@step("el turno no aparece en el calendario")
def shift_deleted(context):
    context.schedules_page.check_shift_deleted()