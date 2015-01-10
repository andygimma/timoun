Feature: Ensure that breadcrumbs are visible
  Scenario: Ensure that breadcrumbs are visible on the home page
    Given I go to "http://localhost:8080"
      When I click on "Home"
      Then I should see "Future Home of Timoun"
      When I click on the "home" breadcrumb
      Then I should see "Future Home of Timoun"
      
  Scenario: Ensure that breadcrumbs are visible on the about page
    Given I go to "http://localhost:8080/about"
      Then I should see "Home > About"
      When I click on the "about" breadcrumb
      Then I should see "About Timoun"
      
  Scenario: Ensure that breadcrumbs are visible on the contact page
    Given I go to "http://localhost:8080/contact"
      Then I should see "Home > Contact"
      When I click on the "contact" breadcrumb
      Then I should see "Contact IBESR"
      
  Scenario: Ensure that breadcrumbs are visible on the suggest services page
    Given I go to "http://localhost:8080/suggest_services"
      Then I should see "Home > Suggest Services"
      When I click on the "suggest_services" breadcrumb
      Then I should see "Suggest Services for Timoun"
      
  Scenario: Ensure that breadcrumbs are visible on the search page
    Given I go to "http://localhost:8080/search"
      Then I should see "Home > Search"
      When I click on the "search" breadcrumb
      Then I should see "Search Timoun"
      
  Scenario: Ensure that breadcrumbs are visible on the mental illness services page
    Given I go to "http://localhost:8080/mental_illness_services"
      Then I should see "Home > Mental Illness Services"
      When I click on the "mental_illness_services" breadcrumb
      Then I should see "Timoun Mental Illness Services"