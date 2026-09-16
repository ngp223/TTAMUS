Feature: Registro de usuario

  @E2E_01
  Scenario: Registrar un nuevo usuario
    Given pulso crear cuenta
    When relleno campos obligatorios
    Then creo usuario
    And el administrador esta en el restaurante

