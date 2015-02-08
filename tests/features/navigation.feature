Feature: Testing the Navigation Bar
  Scenario: Make sure the navigation bar has the correct links
    Given I go to "http://localhost:8080/users/login"
      Then I should see "About"
      Then I should see "Search"
      Then I should see "Contact IBESR"
      Then I should see "Suggest Services"
      Then I should see "Mental Illness Service"
      Then I should see "Login"

  Scenario: Ensure that each nav link works
    Given I go to "http://localhost:8080"
      When I click on "Timoun"
      Then I should see "Future Home of Timoun"
      When I click on "About"
      Then I should see "About Timoun"
      When I click on "Contact IBESR"
      Then I should see "Contact IBESR"
      When I click on "Suggest Services"
      Then I should see "Suggest Services for Timoun"
      When I click on "Mental Illness Services"
      Then I should see "Timoun Mental Illness Services"
