Feature: Backup POS

  Background:
    Given estoy logueado en el POS
  
    Scenario: Crear y eliminar una copia de respaldo
    Then accedo a copia de seguridad
    And creo la copia de respaldo
    And la copia es listada