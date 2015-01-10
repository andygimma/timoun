Feature: Ensure that error codes are properly handled
  Scenario: As a user, if I go to an incorrect url, I should see an error message
    Given I go to "http://localhost:8080/incorrect_url"
      Then I should see "Page not found"
