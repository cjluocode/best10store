from django.shortcuts import render
from items.amazon_models import Item
from .models import FeatureProduct
from items.review_model import Review
# Create your views here.


def product_detail(request, id):
    product = FeatureProduct.objects.get(id=id)
    print(product.link)
    review  = Review()
    reviews = review.parse_reviews(product.link)

    context = {
        'product': product,
        'reviews' : reviews,
    }
    return render(request,'featured_products/product_detail.html', context)




