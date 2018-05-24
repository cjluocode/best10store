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

            if len(search_result) == 0:
                print("where is backup baby")
                search_result = item.get_square_items(q_word)


            context = {
             "item_list": search_result
            }
            return render(request,'items/item_list.html', context)
        else:
            return render(request, 'items/item_list.html')
    else:
        return render(request,'items/item_list.html')
