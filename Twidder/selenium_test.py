# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class SeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:5000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_selenium(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("test@gmail.com")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("newpassword")
        driver.find_element_by_xpath("//input[@value='LogIn']").click()
        driver.find_element_by_xpath("//input[@value='Browse']").click()
        driver.find_element_by_id("otherUserEmail").clear()
        driver.find_element_by_id("otherUserEmail").send_keys("wille@gmail.com")
        driver.find_element_by_xpath("//input[@value='Find user']").click()
        driver.find_element_by_id("otherMessage").clear()
        driver.find_element_by_id("otherMessage").send_keys("test message to other user")
        driver.find_element_by_xpath("(//input[@value='Post'])[2]").click()
        driver.find_element_by_css_selector("input.btn.btn-default").click()
        driver.find_element_by_id("message").clear()
        driver.find_element_by_id("message").send_keys("test message to me")
        driver.find_element_by_id("postButton").click()
        driver.find_element_by_xpath("//input[@value='Account']").click()
        driver.find_element_by_xpath("//input[@value='signOut']").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
