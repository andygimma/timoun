Feature: Ensure that breadcrumbs are visible
  Scenario: Ensure that breadcrumbs are visible on the home page
    Given I go to "http://localhost:8080"
      When I click on "Home"
      Then I should see "Welcome to Timoun"
      When I click on the "home" breadcrumb
      Then I should see "Welcome to Timoun"

  Scenario: Ensure that breadcrumbs are visible on the about page
    Given I go to "http://localhost:8080/about"
      When I click on the "about" breadcrumb
      Then I should see "About Timoun"

  Scenario: Ensure that breadcrumbs are visible on the contact page
    Given I go to "http://localhost:8080/contact"
      When I click on the "contact" breadcrumb
      Then I should see "Contact IBESR"

  Scenario: Ensure that breadcrumbs are visible on the suggest services page
    Given I go to "http://localhost:8080/suggest_services"
      When I click on the "suggest_services" breadcrumb
      Then I should see "Suggest Services for Timoun"

  Scenario: Ensure that breadcrumbs are visible on the search page
    Given I go to "http://localhost:8080/search"
      When I click on the "search" breadcrumb
      Then I should see "Search Timoun"

  Scenario: Ensure that breadcrumbs are visible on the mental illness services page
    Given I go to "http://localhost:8080/mental_illness_services"
      When I click on the "mental_illness_services" breadcrumb
      Then I should see "Timoun Mental Illness Services"
