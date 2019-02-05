from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title> To - Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'), html)

    def test_used_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')



