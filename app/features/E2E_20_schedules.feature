Feature: Schedules POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear, modificar y eliminar un turno
    When accedo a horarios
    Then creo un nuevo turno
    And el turno aparece en el calendario
    And modifico la hora de fin del turno
    And la hora de fin del turno está modificada
    And elimino el turno
    And el turno no aparece en el calendario