from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_used_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListViewTest(TestCase):
    """тест представления списк"""

    def test_used_list_template(self):
        """тест: используется шаблон списка"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        """тест: отображаются элементы только для этого списка"""

        correct_list = List.objects.create()
        Item.objects.create(text='Item 1', list=correct_list)
        Item.objects.create(text='Item 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='другой элемент 1 списка', list=other_list)
        Item.objects.create(text='другой элемент 2 списка', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

        response = self.client.get(f'/lists/{other_list.id}/')

        self.assertContains(response, 'другой элемент 1 списка')
        self.assertContains(response, 'другой элемент 2 списка')

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запро"""

        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запрос"""

        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_passed_correct_list_to_template(self):
        """ест: передается правильный шаблон списк"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    """тест нового списк"""

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """ошибки валидации отсылаются назад в шаблон домашней страницы"""

        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        """тест: сохраняются недопустимые элементы списка """

        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

