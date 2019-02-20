from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape

from lists.forms import ItemForm
from lists.views import home_page
from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR


class HomePageTest(TestCase):

    def test_used_home_template(self):
        """тест: использует домашний шаблон"""

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_uses_home_template(self):
        """тест: домашняя страница использует форму для элемент"""

        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_passed_correct_list_to_template(self):
        """ест: передается правильный шаблон списк"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_exiting_list(self):
        """тест: можно сохранить post-запрос в существующий список"""

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/',
                         data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def post_invalid_input(self):
        """отправляет недопустимый ввод"""
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

    def test_for_invalid_input_noting_saved_to_db(self):
        """тест на недопустимый ввод: ничего не сохраняется в БД"""
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        """тест на недопустимый ввод: отображается шаблон списк"""
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_passed_form_to_template(self):
        """тест на недопустимый ввод: форма передается в шаблон"""
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """тест на недопустимый ввод: на странице показывается ошибка"""
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        """тест отображения формы для элемент"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')


class NewListTest(TestCase):
    """тест нового списк"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос в существующий список"""

        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запрос"""

        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_invalid_list_items_arent_saved(self):
        """тест: сохраняются недопустимые элементы списка """

        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        """тест на недопустимый ввод: отображает домашний шаблон"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        """тест: ошибки валидации выводятся на домашней страниц"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        """тест на недопустимый ввод: форма передается в шаблон"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)




