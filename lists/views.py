from django.http import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/one/')
    return render(request, 'lists/home.html')


def view_list(request):
    """представление списк"""
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})



