Feature: Ensure that all static pages work
  Scenario: Make sure the site's main page loads
    Given I go to "http://localhost:8080"
      Then I should see "Future Home of Timoun"

  Scenario: Ensure that a page exists at the correct link for the about page
    Given I go to "http://localhost:8080/about"
      Then I should see "About Timoun"

  Scenario: Ensure that a page exists at the correct link for the contact page
    Given I go to "http://localhost:8080/contact"
      Then I should see "Contact IBESR"

  Scenario: Ensure that a page exists at the correct link for the suggest services page
    Given I go to "http://localhost:8080/suggest_services"
      Then I should see "Suggest Services for Timoun"

  Scenario: Ensure that a page exists at the correct link for the search page
    Given I go to "http://localhost:8080/search"
      Then I should see "Search Timoun"

  Scenario: Ensure that a page exists at the correct link for the mental illness services page
    Given I go to "http://localhost:8080/mental_illness_services"
      Then I should see "Timoun Mental Illness Services"
