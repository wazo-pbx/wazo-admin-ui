# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import urllib

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec


class Page(object):

    TIMEOUT = 4
    CONFIG = {'base_url': 'https://localhost:9296'}

    def __init__(self, driver):
        self.driver = driver

    def build_url(self, *parts, **kwargs):
        path = '/'.join(parts)
        url = "{}/{}".format(self.CONFIG['base_url'].rstrip('/'), path.lstrip('/'))
        if kwargs:
            url += "?{}".format(urllib.urlencode(kwargs))
        return url

    def wait(self):
        return WebDriverWait(self.driver, self.TIMEOUT)

    def wait_for(self, by, arg):
        condition = ec.presence_of_element_located((by, arg))
        self.wait().until(condition)

    def wait_visible(self, by, arg):
        condition = ec.visibility_of_element_located((by, arg))
        self.wait().until(condition)

    def fill(self, by, arg, value, root=None):
        root = root or self.driver
        element = root.find_element(by, arg)
        if element.tag_name == 'select':
            Select(element).select_by_visible_text(value)
        elif element.get_attribute('type') == 'checkbox':
            if element.is_selected() and value is False:
                element.click()
            elif not element.is_selected() and value is True:
                element.click()
        else:
            element.clear()
            element.send_keys(value)

    def fill_name(self, name, value, root=None):
        self.fill(By.NAME, name, value, root)

    def fill_id(self, id_, value, root=None):
        self.fill(By.ID, id_, value, root)

    def select(self, by, arg, value, root=None):
        root = root or self.driver
        element = root.find_element(by, arg)
        Select(element).select_by_visible_text(value)

    def select_name(self, name, value, root=None):
        self.select(By.NAME, name, value, root)

    def select_id(self, id_, value, root=None):
        self.select(By.ID, id_, value, root)

    def get_value(self, id_, root=None):
        root = root or self.driver
        element = root.find_element_by_id(id_)
        return element.get_attribute('value')

    def get_selected_option_value(self, id_, root=None):
        root = root or self.driver
        element = root.find_element_by_id(id_)
        return Select(element).first_selected_option.get_attribute('value')

    def get_input_name(self, name, root=None):
        root = root or self.driver
        element = root.find_element_by_name(name)
        return InputElement(element)

    def extract_errors(self):
        try:
            container = self.driver.find_element_by_class_name("alert-error")
        except NoSuchElementException:
            return []

        return container.text


class InputElement(WebElement):

    def __init__(self, element):
        super(InputElement, self).__init__(element.parent, element.id)

    def get_error(self):
        errors = self.parent.find_element_by_class_name('with-errors')
        try:
            return errors.find_element_by_css_selector('ul li')
        except NoSuchElementException:
            return errors
