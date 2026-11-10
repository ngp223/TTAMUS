Feature: Menus POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear un nuevo menu
    When accedo al módulo de menus
    Then creo un nuevo menu con datos válidos
    And modifico el menu
    And compruebo el menu modificado
    And borro el menu