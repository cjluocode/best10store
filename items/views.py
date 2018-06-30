from django.shortcuts import render
from random import randint
from featured_products.models import FeatureProduct
from .models import SearchItem
# Create your views here.
from django.shortcuts import render
from .amazon_models import Item

# Home Page
def search_result(request):

    if request.method == "POST":
        q_word = request.POST['query_word']
        category = request.POST.get('category', None)


        if q_word:
            item = Item()
            search_result = item.get_items(q_word=q_word)
            save_product(search_result)

            for item in search_result:

                new_item = SearchItem()
                new_item.title = item.title
                new_item.link  = item.link
                new_item.image = item.image
                new_item.rating_count = item.rating_count
                new_item.rating = item.rating
                new_item.hotscore = item.hotscore
                new_item.price    = item.price
                new_item.query_word = q_word

                new_item.goodreads_url = item.goodreads_url

                new_item.save()

            saved_search_result = SearchItem.objects.filter(query_word=q_word)


            context = {

             "item_list": saved_search_result,

            }
            return render(request,'items/search_result.html', context)

        else:
            context = {
                "error" : "Please enter your search items"
            }
            return render(request,'items/search_result.html', context)


    return render(request, 'items/search_result.html')

def item_detail(request, id):
    item = SearchItem.objects.get(id=id)
    print(item.goodreads_url)
    context = {
        'item': item

    }
    return render(request, 'items/item_detail.html', context)





def save_product(item_list):

    for product in item_list:
        featured_product = FeatureProduct()
        featured_product.title = product.title
        featured_product.link  = product.link
        featured_product.image = product.image
        featured_product.rating = product.rating
        featured_product.rating_count = product.rating_count
        featured_product.hotscore     = product.hotscore
        featured_product.price        = product.price

        featured_product.goodreads_url = product.goodreads_url
        featured_product.query_word   = "Programming"
        featured_product.save()

    return FeatureProduct.objects.all()



