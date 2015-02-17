Feature: Ensure that all admin record pages work
  Scenario: Make sure the admin new record page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/records"
      Then I should see "See Record History"

  Scenario: Make sure the admin new progrm page loads
    Given I sign is as an admin user
      And I go to "http://localhost:8080/admin/records"
      Then I should see "First org"
      When I click on "First org"
      Then I should see "source_de_financement"

