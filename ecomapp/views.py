from django.shortcuts import get_object_or_404, render
from django .http import HttpResponse
from . models import category,product
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
# def home(request):
#     return render(request,'home.html')

def allproducts(request,c_slug=None):
    c_page=None
    products_list=None
    if c_slug!=None: 
        c_page=get_object_or_404(category,slug=c_slug)
        products_list=product.objects.all().filter(category=c_page,available=True)
    else:
        products_list=product.objects.all().filter(available=True)
        c_page=category.objects.all()
    paginator=Paginator(products_list,6)
    try:
        page=int(request.GET.get('page',"1"))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products=paginator.page(paginator.num_pages)
    return render(request,'category.html',{'category':c_page,'product':products})

def prodetail(request,c_slug,product_slug):
    try:
        products=product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':products})


