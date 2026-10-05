Feature: Reservations POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear una nueva reserva
    When accedo a Reservas
    And creo una nueva reserva
    Then veo la reserva creada