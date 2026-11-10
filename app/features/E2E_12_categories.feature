Feature: Categories POS

  Background:
    Given estoy logueado en el POS

  Scenario: Categorías
    When accedo a las categorías
    Then creo una categoría
    And la categoría aparece listada
    And modifico la categoría creada
    And la categoría modificada aparece listada
    And elimino esa categoría


