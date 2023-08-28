from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category,Item
from .forms import AddItemForm, EditItemForm

def items(request):
    query = request.GET.get('query','')
    category_id =request.GET.get('category',0)
    categories =Category.objects.all()
    items =Item.objects.filter(is_sold=False)
    
    if category_id:
        items =items.filter(category_id=category_id)
        
    if query:
        items =items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'item/items.html',{
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def details(request, pk):

    item = get_object_or_404(Item, pk = pk)
    # Gets first 3 items in the same category as the 'item' that are not sold, and excludes the item that has the same primary key
    related_items = Item.objects.filter(category = item.category, is_sold = False).exclude(pk = pk)[:3]

    return render(request, "item/detail.html", {

        "item": item,
        "related_items": related_items

    })

@login_required
def add(request):

    if request.method == "POST":

        form = AddItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit = False)
            item.created_by = request.user
            item.save()

            return redirect("item:detail", pk = item.id)

    else:
    
        form = AddItemForm()

    return render(request, "item/form.html", {

        "form": form,
        "title": "Add Item",
        "button": "Create"

    })

@login_required
def delete(request, pk):

    item = get_object_or_404(Item, pk = pk, created_by = request.user)
    item.delete()

    return redirect("dashboard:index")

@login_required
def edit(request, pk):

    item = get_object_or_404(Item, pk = pk, created_by = request.user)

    if request.method == "POST":

        form = EditItemForm(request.POST, request.FILES, instance = item)

        if form.is_valid():

            item.save()

            return redirect("item:detail", pk = item.id)

    else:

        form = EditItemForm(instance = item)

    return render(request, "item/form.html", {

        "form": form,
        "title": "Edit Item",
        "button": "Update"

    })