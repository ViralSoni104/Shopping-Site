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