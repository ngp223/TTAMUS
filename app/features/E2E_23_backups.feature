Feature: Backups POS

  Background:
    Given estoy logueado en el POS
  
    Scenario: Copias de seguridad
    When accedo a copia de seguridad
    Then creo la copia de respaldo
    And la copia es listada