Feature: Informes POS

  Background:
    Given estoy logueado en el POS

  Scenario: Consultar informe de categorías
    When accedo al módulo de informes
    And accedo al informe de categorías
    Then compruebo el informe de categorías