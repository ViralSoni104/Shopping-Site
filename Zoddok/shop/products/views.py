from django.shortcuts import render, redirect
from .models import Category,Product
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
import string

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


def change_image_resolution(product_image,res1,res2,qualtiy):
    product_image_data = product_image.split('/')
    product_image_data[4] = res1
    product_image_data[5] = res2
    product_image_quality = product_image_data[11].split('=')
    product_image_quality[1] = qualtiy
    product_image_quality = '='.join(product_image_quality)
    product_image_data[11] = product_image_quality
    product_image = '/'.join(product_image_data)
    return product_image

def product_detail(request,id,slug):
    query = request.GET.get('color')
    try:
        product = Product.objects.get(pk=id)
    except:
        return redirect('invalid-url')

    r = requests.get(product.product_link)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent,'html.parser')
    # product_title = soup.find('span',attrs={'class':'B_NuCI'}).text
    product_price = soup.find('div',attrs={'class':'_30jeq3 _16Jk6d'}).text

    product_detail_list = soup.find('script',attrs={'id':'jsonLD'},type='application/ld+json')
    json_data = json.loads(product_detail_list.string)
    product_image  = json_data[0]['image']

    #manually change resolution data in url
    product_image = change_image_resolution(product_image,'880','1056','70')
    
    product_rating = json_data[0]['aggregateRating']['ratingValue']
    # product_total_no_of_reviews = json_data[0]['aggregateRating']['reviewCount']
    

    product_description = {}
    product_short_description = ''
    product_details = {}
    
    short_description_from_details = soup.find('div',attrs={'class':'_1AN87F'})
    if short_description_from_details is not None:
        short_description_from_details = short_description_from_details.text
    else:
        short_description_from_details = ''
    
    total_rating = soup.findAll('span',attrs={'class':'_2_R_DZ'})
    for rs in total_rating:
        total_no_of_ratiing = rs.text
        break

    short_description = soup.findAll('div',attrs={'class':'_1mXcCf RmoJUa'})
    for rs in short_description:
        product_short_description = rs.find('p').text
        break

    description_headers = soup.findAll('div',attrs={'class':'_3qWObK'})
    descriptions = soup.findAll('div',attrs={'class':'_3zQntF'})
    for i, description in enumerate(descriptions):
        product_description[description_headers[i].text.strip()] = description.text.strip()

    detail_headers = soup.findAll('div',attrs={'class':'_2H87wv'})
    details = soup.findAll('div',attrs={'class':'_2vZqPX'})
    for i, detail in enumerate(details):
        product_details[detail_headers[i].text.strip()] = detail.text.strip()

    colors_image_list_div = soup.findAll('div',attrs={'class':'_2C41yO _1pH70n _31hAvz'})
    colors_image_list_name_div = soup.findAll('div',attrs={'class':'_3Oikkn _3_ezix _2KarXJ _31hAvz'})
    colors_all_images= {}
    colors_name = ''
    for n,i in enumerate(colors_image_list_div):
        colors_images = change_image_resolution(i['data-img'],'180','180','50')
        colors_all_images[colors_image_list_name_div[n].text.strip()] = colors_images
        colors_name =colors_name+' '+colors_image_list_name_div[n].text.strip()

    
    size_list_anchor = soup.findAll('a',attrs={'class':'_1fGeJ5 _2UVyXR _31hAvz'})
    all_size_list= []
    for i in size_list_anchor:
        all_size_list.append(i.text)

    category = Category.objects.get(pk=product.category_id)
    category=Category.objects.get(pk=category.id).get_ancestors()
    
    
    liked=check_user_has_prodcut_in_favorites(request,product)
    
    context = {
                'product':product,
                # 'title':product_title,
                'price':product_price,'details':product_detail_list,'total_no_of_rating':total_no_of_ratiing,
                'rating':product_rating,'short_description_from_details':short_description_from_details,
                'short_description':product_short_description,'product_description':product_description,'product_details':product_details,
                'product_category': category,'liked_by_user':liked,'colors':colors_all_images,'sizes':all_size_list,
            }
    if query is not None and query!='' and query in colors_name:
        color_image = change_image_resolution(colors_all_images[query],'880','1056','70')
        context.update({'image':color_image})
    else:
        context.update({'image':product_image})
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
            
        product_list=Product.objects.filter(category_id=category.id)
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