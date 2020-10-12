from django.shortcuts import render, redirect
from .models import Category,Color,Product,Variants,Size,Images,SocialLinks
from mptt.templatetags.mptt_tags import cache_tree_children
import json
from django.template.loader import render_to_string
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
import string 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Max, Min, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from bs4 import BeautifulSoup


# Create your views here.
def get_categories():
    root=Category.objects._mptt_filter(level=0)
    root_nodes = cache_tree_children(root.get_descendants())
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))
        jsonTree = json.dumps(dicts,indent=4)
    return jsonTree

def recursive_node_to_dict(node):
    obj = {'title': node.title,'id': node.pk, 'level': node.level,'slug':node.slug, 'get_absolute_url':node.get_absolute_url(),'children': []}
    for child in node.get_children().select_related():
        obj['children'].append(recursive_node_to_dict(child))
    return obj

def check_user_has_prodcut_in_favorites(request,product):
    liked=False
    if product.favorite.filter(id=request.user.id).exists():
        liked=True
    else:
        liked=False
    return liked

def check_list_of_prodcut_favorite(request,liked,product_list):
    liked=liked
    for p in product_list:
        like=check_user_has_prodcut_in_favorites(request,p)
        if like and p.id not in liked:
            liked[p.id]=like
    return liked

def product_detail(request,id,slug):
    query = request.GET.get('q')
    try:
        product = Product.objects.get(pk=id)
    except:
        return redirect('invalid-url')

    category = Category.objects.get(pk=product.category_id)
    category=Category.objects.get(pk=category.id).get_ancestors()
    images = Images.objects.filter(product_id=id)
    social_links=SocialLinks.objects.filter(product_id=id)
    
    url=''
    product_reviews={}
    for rs in social_links:
        if rs.name == 'Flipkart':
            url = rs.link
            r = requests.get(url)
            htmlContent = r.content
            soup = BeautifulSoup(htmlContent,'html.parser')
            rating = soup.find('div',attrs={'class':'hGSR34 bqXGTW'})
            rating = rating.text
            total_no_of_rating = soup.find('span',attrs={'class':'_38sUEc'})
            total_no_of_rating = total_no_of_rating.text
            reviews = soup.find_all('div',attrs={'class':'_2t8wE0'})
            r={}
            i=0
            for rs in reviews:
                r.__setitem__(i,rs.text)
                i+=1

            product_reviews ={
                'rating':rating,
                'total_no_of_rating':total_no_of_rating,
                'reviews':r,
            }
    
    liked=check_user_has_prodcut_in_favorites(request,product)
    
    context = {'product': product,'product_category': category,
               'images': images,'sociallinks':social_links,'liked_by_user':liked,'product_review':product_reviews
               }

    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    return render(request,'product_details.html',context)




def get_node_from_slug(node):
    for rs in Category.objects.all():
        if rs.slug == node:
            return rs

def category(request,slug):
    slug=slug.split('/')
    sitemap=[]
    
    page = request.GET.get('page', 1)

    found=0
    for rs in slug:
        check_cat=Category.objects._mptt_filter(slug=rs)
        if check_cat:
            found+=1

    if found < len(slug):
        return redirect('invalid-url')
        
    for rs in slug:
        sitemap.append(get_node_from_slug(rs))
    
    if len(slug)>1:
        slug=slug[-1]
    else:
        slug=slug[0]
    
    menu_category=get_categories()
    category = Category.objects._mptt_filter(slug=slug)
    sub_categories=''
    product_list=''
    data_sended=''
    liked={}
    if category.get_descendants():
        sub_categories = cache_tree_children(category.get_descendants())
        paginator = Paginator(sub_categories, 15)
        try:
            sub_categories = paginator.page(page)
        except PageNotAnInteger:
            sub_categories = paginator.page(1)
        except EmptyPage:
            sub_categories = paginator.page(paginator.num_pages)

        data_sended='Category'
    else:
        category=category.get()
        for rs in Category.objects.all():
            if rs.title == category:
                category = rs
                break

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

        if order_by_filter == '' and filter_stock == '':
            product_list=Product.objects.filter(category_id=category.id,price__range=(price_from,price_to))
        elif order_by_filter == '' and filter_stock != '':
            product_list=Product.objects.filter(category_id=category.id,stocks=filter_stock,price__range=(price_from,price_to))
        elif order_by_filter !='' and filter_stock == '':
            product_list=Product.objects.filter(category_id=category.id,price__range=(price_from,price_to)).order_by(order_by_filter)
        elif order_by_filter !='' and filter_stock != ' ':
            product_list=Product.objects.filter(category_id=category.id,stocks=filter_stock,price__range=(price_from,price_to)).order_by(order_by_filter)

        paginator = Paginator(product_list, 15)
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)
        liked=check_list_of_prodcut_favorite(request,liked,product_list)
        data_sended='Products'
    
    context={
        'sitemap':sitemap,
        'datas':data_sended,
        'products':product_list,
        'liked_by_user':liked,
        'sub_categories':sub_categories,
    }
    return render(request,"category_details.html",context)

@login_required
def add_to_favorite(request,id):
    product=Product.objects.get(pk=id)
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
        messages.success(request, "Removed from your Favorites")
    else:
        product.favorite.add(request.user)
        messages.success(request, "Added to your Favorites")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def view_favorites(request):
    product_list=Product.objects.all()
    products=[]
    for p in product_list:
        if p.favorite.filter(id=request.user.id).exists():
            products.append(p)
    return render(request,"your_favorite_list.html",{'products':products})