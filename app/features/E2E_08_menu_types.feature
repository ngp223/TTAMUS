Feature: Menus POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear una nueva carta
    When accedo al módulo de cartas
    Then creo una nueva carta con datos válidos
    And modifico la carta creada
    And compruebo que la modificación se ha hecho
    And borro la carta creada 
