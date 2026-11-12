
Feature: Promotions POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear, modificar y eliminar una promoción
    When accedo a las promociones
    Then creo una promoción
    And la promoción aparece listada
    And modifico la promoción
    And la promoción modificada aparece listada
    And elimino la promoción