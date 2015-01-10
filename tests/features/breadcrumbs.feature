Feature: Ensure that breadcrumbs are visible
  Scenario: Ensure that breadcrumbs are visible on the home page
    Given I go to "http://localhost:8080"
      When I click on "Home"
      Then I should see "Future Home of Timoun"
      
  Scenario: Ensure that breadcrumbs are visible on the about page
    Given I go to "http://localhost:8080/about"
      Then I should see "Home > About"
      
  Scenario: Ensure that breadcrumbs are visible on the contact page
    Given I go to "http://localhost:8080/contact"
      Then I should see "Home > Contact"
      
  Scenario: Ensure that breadcrumbs are visible on the suggest services page
    Given I go to "http://localhost:8080/suggest_services"
      Then I should see "Home > Suggest Services"
      
  Scenario: Ensure that breadcrumbs are visible on the search page
    Given I go to "http://localhost:8080/search"
      Then I should see "Home > Search"
      
  Scenario: Ensure that breadcrumbs are visible on the mental illness services page
    Given I go to "http://localhost:8080/mental_illness_services"
      Then I should see "Home > Mental Illness Services"