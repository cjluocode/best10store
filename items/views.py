from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .amazon_models import Item


# Home Page
def item_list(request):
    if request.method == "POST":
        q_word = request.POST['query_word']
        if q_word:
            item = Item()
            search_result = item.get_items(q_word=q_word)
            context = {
             "item_list": search_result[:10]
            }
            return render(request,'items/item_list.html', context)
        else:
            return render(request, 'items/item_list.html')
    else:
        return render(request,'items/item_list.html')
