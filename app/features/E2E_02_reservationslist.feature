Feature: Reservations POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear y gestionar una nueva reserva
    When accedo a Reservas
    And creo una nueva reserva
    And veo la reserva creada
#    And edito la reserva
    And marco la reserva como llegada
    Then cancelo la reserva
    And no veo la reserva cancelada