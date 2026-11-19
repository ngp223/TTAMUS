from behave import when,then
from features.pages.E2E_22_configuration_guide_page import ConfigurationGuidePage


@when("accedo a la Guía de configuración")
def access_configuration_guide(context):
    context.configuration_guide_page = ConfigurationGuidePage(context.driver)
    context.configuration_guide_page.access_configurationguide()


@then("configuro la Guía de configuración")
def configure(context):
    context.configuration_guide_page.configure()

