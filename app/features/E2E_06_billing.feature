Feature: Facturacion POS

  Background:
    Given estoy logueado en el POS
  
  Scenario: Crear una nueva factura
    When accedo al módulo de facturación
    Then creo una nueva factura con datos válidos
    And la factura se crea correctamente
    And veo la factura en el listado de facturas
