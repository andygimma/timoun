## -*- coding: utf-8 -*-
from lettuce import step, world
from selenium.webdriver.common.alert import Alert

@step(u'When I click on "([^"]*)"')
def when_i_click_on_group1(step, keyword):
    world.browser.find_element_by_link_text(keyword).click()
    world.browser.implicitly_wait(2)

@step(u'When I click on the "([^"]*)" breadcrumb')
def when_i_click_on_the_group1_breadcrumb(step, keyword):
    world.browser.find_element_by_id("breadcrumb_" + str(keyword)).click()
    world.browser.implicitly_wait(2)

@step(u'And I wait "([^"]*)" seconds')
def and_i_wait_group1_seconds(step, seconds):
    world.browser.implicitly_wait(seconds)

@step(u'Given I sign is as an admin user')
def given_i_sign_is_as_an_admin_user(step):
    world.browser.get("http://localhost:8080/users/login")
    world.browser.implicitly_wait(2)
    world.browser.find_element_by_id("email").send_keys("admin@example.com")
    world.browser.find_element_by_id("password").send_keys("secret")
    world.browser.find_element_by_id("submit").click()
    world.browser.implicitly_wait(2)

@step(u'When I change "([^"]*)" to "([^"]*)" on the form')
def when_i_change_group1_to_group2_on_the_form(step, element, value):
    world.browser.find_element_by_id(element).clear()
    world.browser.find_element_by_id(element).send_keys(value)


@step(u'When I click "([^"]*)" and confirm the popup')
def when_i_click_group1_and_confirm_the_popup(step, element):
    pass
    #try:
      #world.browser.find_element_by_link_text(element).click()
      #world.browser.execute_script("$('#delete-user').find('a').trigger('click'); ")
      #alert = world.browser.switch_to.alert


    #except:
      #raise Exception(1)

