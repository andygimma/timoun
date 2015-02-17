Feature: Ensure that all admin program pages work
  Scenario: Make sure the admin new progrm page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/programs/new"
      Then I should see "New Program"

  Scenario: I should be able to create a new program, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/programs/new"
      And I fill in "name" with "Program name"
      When I press "Submit"
      And I wait "2" seconds
      And I go to "http://localhost:8080/admin/programs"
      Then I should see "Program name"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Program name"
      And I should see "Create Program"


  Scenario: I should be able to view an existing program
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/programs"
      Then I should see "Program name"
      When I click on "Program name"
      Then I should see "Program name Profile"
      And I should see "Name"

  Scenario: I should be able to edit an existing user, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/programs"
      Then I should see "Program name"
      When I click on "Program name"
      Then I should see "Program name Profile"
      When I change "name" to "Program edit" on the form
      And I press "Submit"
      Then I should see "Program updated successfully"
      And I go to "http://localhost:8080/admin/programs"
      And I should see "Program edit"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Edit Program"

  Scenario: I should be able to see the Audit page for Programs
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/programs"
      When I click on "See Program Changes"
      Then I should see "Program Affected"

  Scenario: I should be able to delete an existing program, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/programs"
      Then I should see "Program edit"
      When I click on "Program edit"
      Then I should see "Program edit Profile"
      When I click "Delete Program" and confirm the popup
      And I wait "2" seconds
      Then I should see "deleted"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Delete Program"
