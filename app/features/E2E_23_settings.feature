Feature: Settings POS

  Background:
    Given estoy logueado en el POS

  Scenario: Acceder a los ajustes
    When accedo a los ajustes
    Then defino ajustes generales
    And defino la apariencia
    And defino la accesibilidad
    And defino notificaciones
    And defino impuestos
    And defino negocio
    And defino cuenta