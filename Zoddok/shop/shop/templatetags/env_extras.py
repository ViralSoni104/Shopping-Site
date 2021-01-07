import os
from django import template
from products.views import get_categories
import json
from products.models import Category
from shop.models import SiteSetting
import urllib.parse as urlparse
from urllib.parse import urlencode
import string
from shop.models import Team
from django.urls import reverse
import requests
from bs4 import BeautifulSoup


register = template.Library()


@register.simple_tag
def get_team():
    return Team.objects.all()

@register.simple_tag
def get_env_var(key):
    return os.environ.get(key)

@register.simple_tag
def get_site_setting():
    Site_Setting=SiteSetting.objects.all().order_by('-id')[:1]
    Site_Setting=Site_Setting[0]
    return Site_Setting


@register.simple_tag
def get_product_details(product_link):
    r = requests.get(product_link)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent,'html.parser')
    # product_title = soup.find('span',attrs={'class':'B_NuCI'}).text
    product_price = soup.find('div',attrs={'class':'_30jeq3 _16Jk6d'}).text
    product_detail_list = soup.find('script',attrs={'id':'jsonLD'},type='application/ld+json')
    json_data = json.loads(product_detail_list.string)
    product_image  = json_data[0]['image']

    #manually change resolution data in url
    product_image_data = product_image.split('/')
    product_image_data[4] = '320'
    product_image_data[5] = '480'
    product_image = '/'.join(product_image_data)
    
    rs={
        # 'title':product_title,
        'price':product_price,'image':product_image,
    }
    return rs




@register.filter(name='times') 
def times(number):
    return range(len(number))

@register.filter(name='var_length') 
def var_length(number):
    return (len(number)-1)

@register.simple_tag
def get_node_value(node_list,index):
    return node_list[index]

@register.simple_tag
def get_node_url(node_list,index):
    node=get_node_value(node_list,index)
    return node.get_absolute_url()

@register.simple_tag
def get_category(category_id):
    category=Category.objects.get(pk=category_id)
    return category.get_absolute_url()

@register.simple_tag(takes_context = True)
def query_transform(context,url,param_name,param_value):
    if '?' in url:
        if param_name in url:
           return query_transform_with_cust_url(url,param_name,param_value)
        else:
            return url+"&"+param_name+"="+param_value
    else:
        return url+"?"+param_name+"="+param_value

@register.simple_tag(takes_context = True)
def query_transform_with_cust_url(url,param_name,param_value):
    url=url.split("?")
    url2=url[1].split("&")
    new_url='?'
    i=0
    max_len_url=len(url2)-1
 
    for x in url2:
        splited=x.split("=")
        
        if splited[0] == param_name:
            x=splited[0]+"="+param_value

        if i == max_len_url:
            new_url+=x
        else:
            new_url+=x+"&"
        i+=1

    return new_url

@register.simple_tag()
def remove_to(url,param_name):
    url=url.split("?")
    url2=url[1].split("&")
    new_url='?'
    i=0
    max_len_url=len(url2)-1
 
    for x in url2:
        splited=x.split("=")
        
        if splited[0] == param_name:
            if i == max_len_url:
                new_url=new_url[:-1]
            i+=1
            continue
        else:
            x=splited[0]+"="+splited[1]
        
        if i == max_len_url:
            new_url+=x
        else:
            new_url+=x+"&"
        i+=1    
    return new_url

@register.inclusion_tag('nav.html')
def show_categories():
      category =json.loads(get_categories())
      return { 'category' : category }
