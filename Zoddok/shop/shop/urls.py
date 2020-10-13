"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from accounts import views as accountViews
from django.contrib.auth import views as auth_views #import this
from products import views as productViews
from . import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('accounts/',accountViews.accountView,name='accounts'),
    path('accounts/signup/',accountViews.signup,name='signup'),
    path('accounts/login/',accountViews.loginUser,name='login'),
    path('accounts/logout/',accountViews.logoutUser,name='logout'),
    path('activate/<uidb64>/<token>/',accountViews.activate, name='activate'),
    path('validateEmail/',accountViews.validateEmail,name='validateEmail'),
    path('validateName/',accountViews.name_validate,name='validateName'),
    path('validatePass/',accountViews.validatePass,name='validatePass',),
    path('numericPass/',accountViews.numericPass,name='numericPass',),
    path('comparePass/',accountViews.comparePass,name='comparePass',),
    path('commanPass/',accountViews.commanPassCheck,name='commanPass',),
    path('accounts/forget-password/',accountViews.forget_pass_view,name='forget-password'),
    path('accounts/forget-password-confirm/<uidb64>/<token>/',accountViews.forget_pass_comfirm_view, name='forget-password-confirm'),
    path('accounts/change-password/',accountViews.change_password,name='change-password'),
    path('page-not-found/',views.invalid_url_view,name='invalid-url'),
    re_path(r'^category/(?P<slug>.*)/$',productViews.category,name='category'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('product/<int:id>/<slug:slug>',productViews.product_detail,name="product-details"),
    path('addfavorite/<int:id>',productViews.add_to_favorite,name='add-favorite'),
    path('favorites/',productViews.view_favorites,name='your-favorites'),
    path('about-us/',views.about_view,name="about"),
    path('contact-us/',views.contact_view,name="contact"),
    path('search_auto/',views.search_auto,name="search_auto"),
    path('search/',views.search,name="search"),
    path('FAQ/',views.FAQ_View,name="faq"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)