# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from selenium import webdriver
from pyvirtualdisplay import Display

from .index import IndexPage
from .login import LoginPage


class Browser(object):

    pages = {'index': IndexPage,
             'login': LoginPage}

    def __init__(self, username, password, virtual=True):
        self.username = username
        self.password = password
        self.display = Display(visible=virtual, size=(1024, 768))

    def start(self):
        self.display.start()
        self.driver = webdriver.Firefox(capabilities={'marionette': False})
        self.driver.set_window_size(1024, 768)
        self._login()

    def _login(self):
        LoginPage(self.driver).login(self.username, self.password)

    def logout(self):
        LoginPage(self.driver).logout()

    def __getattr__(self, name):
        page = self.pages[name](self.driver)
        return page.go()

    def stop(self):
        self.driver.close()
        self.display.stop()
