Feature: Users POS

  Background:
    Given estoy logueado en el POS

  Scenario: Crear, modificar y eliminar un usuario
    When accedo a usuarios
    Then creo un nuevo usuario
    And el usuario aparece en el listado
    And modifico el usuario
    And el usuario modificado aparece en el listado
    And desactivo el usuario
    And el usuario no aparece en el listado