Feature: Closure history POS

  Background:
    Given estoy logueado en el POS
    
  Scenario: Historial de cierres
    When accedo al historial de cierres
    Then veo el cierre en el historial
    