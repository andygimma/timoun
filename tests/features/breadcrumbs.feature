Feature: Ensure that breadcrumbs are visible
  Scenario: Ensure that breadcrumbs are visible on the home page
    Given I go to "http://localhost:8080"
      When I click on "Home"
      Then I should see "Future Home of Timoun"