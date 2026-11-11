
Feature: Products POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear, modificar y eliminar un producto
    When accedo a los productos
    Then creo un producto
    And el producto aparece listado
    And modifico ese producto
    And el producto modificado aparece listado
    And elimino el producto
