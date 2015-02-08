Feature: Ensure that the admin dashboard pages work
  Scenario: Make sure the admin new organization page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Initiated By"

  Scenario: Make sure the admin new organization page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/dashboard"
      When I click on "View"
      Then I should see "Dashboard Item"

