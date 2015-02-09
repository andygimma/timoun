Feature: Ensure that all admin service pages work
  Scenario: Make sure the admin new service page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/services/new"
      Then I should see "New Service"

  Scenario: I should be able to create a new service, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/services/new"
      And I fill in "name" with "Service name"
      When I press "Submit"
      And I wait "2" seconds
      And I go to "http://localhost:8080/admin/services"
      Then I should see "Service name"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Service name"
      And I should see "Create Service"


  Scenario: I should be able to view an existing service
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/services"
      Then I should see "Service name"
      When I click on "Service name"
      Then I should see "Service name Profile"
      And I should see "Name"

  Scenario: I should be able to edit an existing service, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/services"
      Then I should see "Service name"
      When I click on "Service name"
      Then I should see "Service name Profile"
      When I change "name" to "Service edit" on the form
      And I press "Submit"
      Then I should see "Service updated successfully"
      And I go to "http://localhost:8080/admin/services"
      And I should see "Service edit"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Edit Service"

  Scenario: I should be able to see the Audit page for Services
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/services"
      When I click on "See Service Changes"
      Then I should see "Service Affected"

  Scenario: I should be able to delete an existing service, and see it reflected on the Audit page
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/services"
      Then I should see "Service edit"
      When I click on "Service edit"
      Then I should see "Service edit Profile"
      When I click "Delete Service" and confirm the popup
      And I wait "2" seconds
      Then I should see "deleted"
      When I go to "http://localhost:8080/admin/dashboard"
      Then I should see "Delete Service"
