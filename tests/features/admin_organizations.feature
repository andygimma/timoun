Feature: Ensure that all admin organization pages work
  Scenario: Make sure the admin new organization page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/organizations/new"
      Then I should see "New Organization"

  Scenario: I should be able to create a new user, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/organizations/new"
      And I fill in "name" with "Org name"
      When I press "Submit"
      And I wait "2" seconds
      And I go to "http://localhost:8080/admin/organizations"
      Then I should see "Org name"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Org name"
      And I should see "Create Organization"


  Scenario: I should be able to view an existing user
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/organizations"
      Then I should see "Org name"
      When I click on "Org name"
      Then I should see "Org name Profile"
      And I should see "Name"

  Scenario: I should be able to edit an existing user, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/organizations"
      Then I should see "Org name"
      When I click on "Org name"
      Then I should see "Org name Profile"
      When I change "name" to "Org edit" on the form
      And I press "Submit"
      Then I should see "Organization updated successfully"
      And I go to "http://localhost:8080/admin/organizations"
      And I should see "Org edit"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Edit Organization"

  Scenario: I should be able to see the Audit page for Organizations
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/organizations"
      When I click on "See Organization Changes"
      Then I should see "Organization Affected"
