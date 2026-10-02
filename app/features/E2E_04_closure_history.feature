Feature: Historial de Cierres POS

  Background:
    Given estoy logueado en el POS
    
  Scenario: Acceso al historial de tickets
    When accedo al historial de cierres
    Then veo el cierre en el historial
    
    

    
    
    