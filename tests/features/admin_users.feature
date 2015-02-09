Feature: Ensure that all admin user pages work
  Scenario: Make sure the admin new user page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/users/new"
      Then I should see "New User"

  Scenario: I should be able to create a new user, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/users/new"
      When I fill in "email" with "user2@example.com"
      And I fill in "name" with "Admin name"
      And I fill in "organization" with "Ibesr Haiti"
      And I fill in "phone" with "1234567890"
      And I select "admin" from "role"
      When I press "Submit"
      And I wait "2" seconds
      And I go to "http://localhost:8080/admin/users"
      Then I should see "user2@example.com"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "user2@example.com"

  Scenario: I should be able to view an existing user
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/users"
      Then I should see "user2@example.com"
      When I click on "user2@example.com"
      Then I should see "user2@example.com Profile"
      And I should see "Name"
      And I should see "Organization"
      And I should see "Phone"

  Scenario: I should be able to edit an existing user, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/users"
      Then I should see "user2@example.com"
      When I click on "user2@example.com"
      Then I should see "user2@example.com Profile"
      When I change "organization" to "Vision Link" on the form
      And I press "Submit"
      Then I should see "Profile updated successfully"
      And I go to "http://localhost:8080/admin/users"
      And I should see "Vision Link"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Update User"

  Scenario: When I am on the admin users page, I should be able to see User audits
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/users"
      When I click on "See User Changes"
      Then I should see "Security Clearance"
      And I should see "Create User"
      And I should see "Update User"

  Scenario: I should be able to delete an existing user, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/users"
      Then I should see "user2@example.com"
      When I click on "user2@example.com"
      Then I should see "user2@example.com Profile"
      When I click "Delete User" and confirm the popup
      And I wait "2" seconds
      Then I should see "deleted"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Delete User"
