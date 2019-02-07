import time

from selenium import webdriver
import unittest
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To - Do lists', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('To - Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item'
                         )
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Купить павлиньи перья')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item'
                         )
        inputbox.send_keys('Сделать мушку из павлиньих перье')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Купить павлиньи перья')
        self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перье')

        self.fail('Закончить тест')

