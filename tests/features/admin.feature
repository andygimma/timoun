Feature: Ensure that all admin pages work
  Scenario: Make sure the site's main page loads
    Given I go to "http://localhost:8080/admin"
      Then I should see "Future Home of the Admin Console"

  Scenario: Make sure the admin user index loads
    Given I go to "http://localhost:8080/admin/users"
      Then I should see "Add User"

  Scenario: Make sure the admin new user page loads
    Given I go to "http://localhost:8080/admin/users/new"
      Then I should see "New User"
      When I fill in "email" with "user2@example.com"
      And I fill in "name" with "Admin name"
      And I fill in "organization" with "Ibesr Haiti"
      And I fill in "phone" with "1234567890"
      And I select "other" from "role"
      When I press "Submit"
      And I wait "3" seconds
      And I go to "http://localhost:8080/admin/users"
      Then I should see "user2@example.com"
