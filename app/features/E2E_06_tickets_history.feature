Feature: Tickets history POS

  Background:
    Given estoy logueado en el POS
    
  Scenario: Acceso al historial de tickets
    When accedo al historial de tickets
    Then veo el historial de tickets
    
    
