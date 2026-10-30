Feature: Cash Closure POS

  Background:
    Given estoy logueado en el POS
    
  Scenario: Cierre de caja completo
    When accedo al cierre de caja
    Then realizo el cierre de caja