Feature: Reports POS

  Background:
    Given estoy logueado en el POS

  Scenario: Informes, categorías
    When accedo al módulo de informes
    And accedo al informe de categorías
    Then compruebo el informe de categorías