Feature: Categories POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear, modificar y eliminar una categoría
    When accedo a las categorías
    Then creo una categoría
    And la categoría aparece listada
    And modifico la categoría creada
    And la categoría modificada aparece listada
    And elimino esa categoría


