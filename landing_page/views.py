from django.shortcuts import render
from featured_products.models import FeatureProduct
from datetime import datetime, timedelta
from items.models import SearchItem
# Create your views here.

def home(request):
    featured_products = FeatureProduct.objects.filter(query_word="Startup")
    delete_older_items()

    item_list = []

    if request.method == "GET":
        category = request.GET.get('category')
        if not category:
            category= 'Startup'
        if category:
            featured_products = FeatureProduct.objects.filter(query_word=category)

            context = {
                'featured_products': featured_products,
                'category': category,
            }
            return render(request, 'landing_page/home.html', context)


    return render(request, 'landing_page/home.html',{'featured_products': featured_products})



def delete_older_items():
    time_threshold = datetime.now() - timedelta(minutes=1)
    results = SearchItem.objects.filter(created_at__lt=time_threshold)
    if results:
        print('Deleted ' + str(len(results)) + " old items")
        results.delete()



def about(request):
    return render(request,'landing_page/about.html')

def contact(request):
    return render(request,'landing_page/contact.html')

