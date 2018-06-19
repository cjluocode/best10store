from django.shortcuts import render
from .models import Blog
# Create your views here.

def blog_list(request):
    blogs = Blog.objects.all().order_by('-id')

    context = {
        'blogs': blogs
    }

    return render(request, 'blogs/blog_list.html',context)

def blog_detail(request, id):

    blog = Blog.objects.get(id=id)

    context = {
        'blog': blog
    }

    return render(request, 'blogs/blog_detail.html',context)

def testing(request):
    return render(request, 'blogs/testing.html')




