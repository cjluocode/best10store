from django.shortcuts import render
from items.amazon_models import Item
from .models import FeatureProduct
# Create your views here.


def product_detail(request, id):
    product = FeatureProduct.objects.get(id=id)

    context = {
        'product': product,
    }
    return render(request,'featured_products/product_detail.html', context)




