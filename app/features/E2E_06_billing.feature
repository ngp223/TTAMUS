Feature: Billing POS

  Background:
    Given estoy logueado en el POS
  
  Scenario: Facturación
    When accedo al módulo de facturación
    Then creo una nueva factura con datos válidos
    And veo la factura en el listado de facturas
