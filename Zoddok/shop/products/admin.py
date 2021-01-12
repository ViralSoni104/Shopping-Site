from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Product, Category
import admin_thumbnails
# Register your models here.

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title','related_products_count', 'related_products_cumulative_count','image_tag')
    list_display_links = ('indented_title',)
    search_fields = ('name',)
    list_filter = ('status','create_at','update_at')
    actions = ['make_published','make_unpublished']
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

    def make_published(modeladmin, request, queryset):
        queryset.update(status='True')
    make_published.short_description = "Make Category Visible To User"
    

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(status='False')
    make_unpublished.short_description = "Hide Category From User"


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