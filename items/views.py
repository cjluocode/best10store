from django.shortcuts import render
from random import randint

# Create your views here.
from django.shortcuts import render
from .amazon_models import Item

# Home Page
def item_list(request):
    total_items_number = randint(239, 278)

    if request.method == "POST":
        q_word = request.POST['query_word']
        if q_word:
            item = Item()
            search_result = item.get_items(q_word=q_word)
            context = {
             "item_list": search_result,
             "total_items_number" : total_items_number,
            }
            return render(request,'items/item_list.html', context)
        else:
            return render(request, 'items/item_list.html')
    else:
        return render(request,'items/item_list.html')
