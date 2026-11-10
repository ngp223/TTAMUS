Feature: Modifiers POS

  Background:
    Given estoy logueado en el POS

  Scenario: Modificadores
    When accedo a los modificadores
    Then creo un modificador
    And el modificador aparece listado
    And modifico el modificador
    And el modificador modificado aparece listado
    And elimino el modificador

    