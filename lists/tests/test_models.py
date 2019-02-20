from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item, List


class ItemModelTest(TestCase):
    """тест модели элемента"""

    def test_cannot_save_empty_list_items(self):
        """ест: нельзя добавлять пустые элементы списк"""

        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_validate_fields_in_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.clean_fields()

    def test_duplicate_items_are_invalid(self):
        """тест: повторы элементов не допустимы"""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(IntegrityError):
            item = Item(list=list_, text='bla')
            # item.full_clean()
            item.save()

    def test_CAN_save_same_item_to_different_lists(self):
        """тест: МОЖЕТ сохранить тот же элемент в разные списка"""
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # не должен поднать исключение

    def test_list_aordering(self):
        """тест упорядочения списк"""
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self):
        """тест строкового представления"""
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

    def test_default_text(self):
        """'тест заданного по умолчанию текста"""
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        """тест: элемент связан co списком"""
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())


class ListModelTest(TestCase):
    """тест модели списка"""

    def test_get_absolute_url(self):
        """тест: получен абсолютный url"""

        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

