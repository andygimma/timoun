Feature: Testing the Navigation Bar
  Scenario: Make sure the navigation bar has the correct links
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin"
      Then I should see "Users"
      When I click on "Users"
      Then I should see "Add User"

