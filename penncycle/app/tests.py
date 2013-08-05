from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
# import time
class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super(MySeleniumTests, cls).tearDownClass()

    # def test_login(self)
    #     self.selenium.get(self.live_server_url + '/signup/')
    #     username_input = self.selenium.find_element_by_name("username")
    #     username_input.send_keys('myuser')
    #     password_input = self.selenium.find_element_by_name("password")
    #     password_input.send_keys('secret')
    #     # self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
    #     assert 1 == 1

    def test_signup(self):
        self.selenium.get(self.live_server_url + '/signup/')
        self.selenium.find_element_by_id("id_penncard").send_keys("44060599")
        self.selenium.find_element_by_id("id_name").send_keys("Test Student")
        self.selenium.find_element_by_id("id_phone").send_keys("9999993124")
        self.selenium.find_element_by_id("id_email").send_keys("test@test.com")
        el = self.selenium.find_element_by_id("id_grad_year")
        el.click()
        option = el.find_elements_by_tag_name("option")[1]
        option.click()
        el = self.selenium.find_element_by_id("id_living_location")
        el.click()
        option = el.find_elements_by_tag_name("option")[1]
        option.click()
        self.selenium.find_element_by_id("id_gender_1").click()
        self.selenium.find_element_by_id("submit-id-submit").click()
        assert True

    def test_user_login(self):
        pass
