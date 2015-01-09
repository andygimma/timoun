Feature: Testing the Navigation Bar
  Scenario: Make sure the navigation bar has the correct links
    Given I go to "http://localhost:8080"
      Then I should see "About"
      Then I should see "Search"
      Then I should see "Contact IBESR"
      Then I should see "Suggest Service"
      Then I should see "Mental Illness Service"
      Then I should see "Login"
