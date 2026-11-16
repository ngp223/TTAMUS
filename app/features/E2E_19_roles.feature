Feature: Roles POS

  Background:
    Given estoy logueado en el POS
      
  Scenario: Crear, modificar y eliminar un rol
    Given estoy logueado en el POS
    When accedo a roles
    Then creo un nuevo rol
    And el rol aparece en el listado
    And modifico el rol
    And el rol modificado aparece en el listado
    And elimino el rol
    And el rol no aparece en el listado