Feature: Visiting the home page
  Scenario: Make sure the site's main page loads
    Given I go to "http://localhost:8080"
      Then I should see "Future Home of Timoun"