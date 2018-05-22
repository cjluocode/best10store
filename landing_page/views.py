from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request,'landing_page/about.html')

def contact(request):
    return render(request,'landing_page/contact.html')

