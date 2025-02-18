from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, Category
import admin_thumbnails
# Register your models here.

class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ('title', 'parent', 'status')



class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_title','category', 'status','feature_to_home_page']
    list_filter = ['category']
    actions = ['make_published','make_unpublished']
    prepopulated_fields = {'slug': ('product_title',)}
    def make_published(modeladmin, request, queryset):
        queryset.update(status='True')
    make_published.short_description = "Make Product Visible To User"
    

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(status='False')
    make_unpublished.short_description = "Hide Product From User"

admin.site.register(Product,ProductAdmin)
admin.site.register(Category, CategoryAdmin)