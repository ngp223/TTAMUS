Feature: Backups POS

  Background:
    Given estoy logueado en el POS
  
    Scenario: Copias de seguridad
    Then accedo a copia de seguridad
    And creo la copia de respaldo
    And la copia es listada