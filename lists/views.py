from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.forms import ItemForm, ExitingListItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'lists/home.html', context={'form': ItemForm()})


def view_list(request, list_id):
    """представление списка"""
    list_ = List.objects.get(id=list_id)
    form = ExitingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExitingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, 'form': form})


def new_list(request):
    """новый список"""
    form = ItemForm(data=request.POST)

    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form': form})

