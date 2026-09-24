Feature: Reservations POS

  Background:
    Given estoy logueado en el POS

  Scenario: Venta completa con pago
    When selecciono la mesa
    And selecciono comensales
    And selecciono el producto
    And aumento la cantidad del producto
    Then realizo el pago


