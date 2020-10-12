from django.shortcuts import render, redirect
from urllib import request
from products.models import Category, Product
from products.views import check_user_has_prodcut_in_favorites, check_list_of_prodcut_favorite
from .forms import ContactForm
from shop import custom_messages as Custom_Msg
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .templatetags.env_extras import get_env_var
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.views import check_user_has_prodcut_in_favorites, check_list_of_prodcut_favorite
from django.db.models import Avg, Max, Min, Sum
from mptt.templatetags.mptt_tags import cache_tree_children, get_cached_trees
from collections import OrderedDict 

#home page view
def home(request):
    category=Category.objects.filter(feature_to_home_page='Yes')
    latest_products=Product.objects.all().order_by('-id')[:4]
    featured_products=Product.objects.filter(feature_to_home_page='Yes')
    liked={}
    liked=check_list_of_prodcut_favorite(request,liked,latest_products)
    liked=check_list_of_prodcut_favorite(request,liked,featured_products)
    context = { 'featured_category' : category , 'latest_products' : latest_products,'featured_products' : featured_products,'liked_by_user':liked}
    return render(request,'index.html',context)

#invalid url page view
def invalid_url_view(request):
    return render(request,'404.html')


#about us page view
def about_view(request):
    return render(request,'about_us.html')

#contact us page view
def contact_view(request):
    form=ContactForm()
    if request.method == 'POST':
        form=ContactForm(data=request.POST)
        if form.is_valid():
            name=request.POST.get('contact_name')
            mail_subject = 'Contact Form Submission By Customer '+name
            from_email=request.POST.get('contact_email')
            message="Customer Name : "+name+"\n\nMail customer by clicking below mail id\n"+from_email+"\n\nCustomer Message : "+request.POST.get('message')
            try:
                send_mail(mail_subject, message,from_email,[get_env_var('EMAIL_HOST_USER'),])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            form.save()
            messages.success(request,Custom_Msg.CONTACT_MAIL_SENT)
            return redirect('contact')
    return render(request,'contact_us.html',{'form':form})

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('search', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title + " -> " + rs.category.title 
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        liked={}
        order_by_filter=''
        filter_stock=''
        price_from=0
        price_to=Product.objects.all().aggregate(Max('price'))['price__max']

        if request.GET.get('ordering','') == 'title' or request.GET.get('ordering','') == '-title' or request.GET.get('ordering','') == '-price'  or request.GET.get('ordering','') == 'price':
            order_by_filter=request.GET.get('ordering','')
        if request.GET.get('availabel','') == 'In-Stock' or request.GET.get('availabel','') == 'Include-Out-Of-Stock':
            filter_stock=request.GET.get('availabel','')
            if request.GET.get('availabel','') == 'Include-Out-Of-Stock':
                filter_stock=''
        if request.GET.get('price_from','') != '':
            price_from=request.GET.get('price_from')
        if request.GET.get('price_to','') != '':
            price_to=request.GET.get('price_to')

        page = request.GET.get('page', 1)

        if order_by_filter == '' and filter_stock == '':
            product_list=Product.objects.filter(title__icontains=query,price__range=(price_from,price_to))
        elif order_by_filter == '' and filter_stock != '':
            product_list=Product.objects.filter(title__icontains=query,stocks=filter_stock,price__range=(price_from,price_to))
        elif order_by_filter !='' and filter_stock == '':
            product_list=Product.objects.filter(title__icontains=query,price__range=(price_from,price_to)).order_by(order_by_filter)
        elif order_by_filter !='' and filter_stock != ' ':
            product_list=Product.objects.filter(title__icontains=query,stocks=filter_stock,price__range=(price_from,price_to)).order_by(order_by_filter)
        
        paginator = Paginator(product_list, 15)
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)
        sub_cat = []
        for rs in product_list:
            sub_cat.append(rs.category)
        
        res = list(OrderedDict.fromkeys(sub_cat))  
        liked=check_list_of_prodcut_favorite(request,liked,product_list)
        context = {
            'sitemap':query,
            'sub_categories':res,
            'products':product_list,
            'liked_by_user':liked
        }
        return render(request, 'search.html', context)