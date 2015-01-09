Feature: Ensure that breadcrumbs are visible
  Scenario: Ensure that breadcrumbs are visible on the home page
    Given I go to "http://localhost:8080"
      Then I should see a link that contains the text "Home" and the url "/"
      When I click on "Home"
      Then I should see "Future Home of Timoun"