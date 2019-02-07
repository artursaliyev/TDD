from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_used_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """тест представления списк"""

    def test_used_list_template(self):
        """тест: используется шаблон списка"""
        response = self.client.get('/lists/one/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_all_list_items(self):
        """тест: отображаются все елементы списка"""

        list_ = List.objects.create()
        Item.objects.create(text='Item 1', list=list_)
        Item.objects.create(text='Item 2', list=list_)

        response = self.client.get('/lists/one/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запро"""

        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запрос"""

        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/lists/one/")


