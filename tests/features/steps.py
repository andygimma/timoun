# -*- coding: utf-8 -*-
from lettuce import step, world

@step(u'When I click on "([^"]*)"')
def when_i_click_on_group1(step, keyword):
    world.browser.find_element_by_link_text(keyword).click()
    world.browser.implicitly_wait(2)
    
