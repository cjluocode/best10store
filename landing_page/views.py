from django.shortcuts import render
from featured_products.models import FeatureProduct
# Create your views here.

def home(request):
    featured_products = FeatureProduct.objects.filter(query_word="Startup")

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



def about(request):
    return render(request,'landing_page/about.html')

def contact(request):
    return render(request,'landing_page/contact.html')

