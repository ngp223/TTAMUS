Feature: Tables map POS

  Background:
    Given estoy logueado en el POS

  Scenario: Mapa de mesas
    When accedo al modulo de mapa de mesas
    Then creo una nueva zona
    And creo una nueva mesa
    And modifico la zona
    And modifico la mesa
    And borro la mesa
    And borro la zona