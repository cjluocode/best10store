from django.shortcuts import render

# Create your views here.

def item_list(request):
    return render(request, 'items/item_list.html')