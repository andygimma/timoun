# -*- coding: utf-8 -*-
from lettuce import step, world

@step(u'When I click on "([^"]*)"')
def when_i_click_on_group1(step, keyword):
    world.browser.find_element_by_link_text(keyword).click()
    world.browser.implicitly_wait(2)
    
@step(u'When I click on the "([^"]*)" breadcrumb')
def when_i_click_on_the_group1_breadcrumb(step, keyword):
    world.browser.find_element_by_id("breadcrumb_" + str(keyword)).click()
    world.browser.implicitly_wait(5)

