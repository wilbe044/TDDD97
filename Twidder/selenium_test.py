from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

__author__ = 'wille'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

def setUp(self):
    self.driver = webdriver.Firefox()
    self.driver.implicitly_wait(30)
    self.base_url = "http://127.0.0.1:5000/"
    self.verificationErrors = []
    self.accept_next_alert = True

class PythonTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()


    def selenium_test_py(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("logInEmail").clear()
        driver.find_element_by_id("logInEmail").send_keys("selenium@mail.com")
        driver.find_element_by_id("logInPassword").clear()
        driver.find_element_by_id("logInPassword").send_keys("password")
        driver.find_element_by_id("logInSubmit").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to.alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True



    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()