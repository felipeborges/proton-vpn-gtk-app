Feature: Login

  Scenario: Successful login without 2FA.
    Given a user without 2FA enabled
    And keyring is unlocked
    And the user is not logged in
    When the correct username and password are introduced in the login form
    And the login form is submitted
    Then the user should be logged in
    Then the credentials are stored in the system's keyring.


  Scenario: Successful login with 2FA.
    Given a user with 2FA enabled
    And the user is not logged in
    When the correct username and password are introduced in the login form
    And the login form is submitted
    And a correct 2FA code is submitted
    Then the user should be logged in.

  Scenario: Wrong password.
    Given the user is not logged in
    When the wrong password is introduced
    And the login form is submitted
    Then the user should be notified with the error message: "Wrong credentials."

  Scenario: Username and password not provided.
    Given the user is not logged in
    When the login data is not provided
    Then the user should not be able to submit the form.
