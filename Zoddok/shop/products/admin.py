from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Product, Category, Color, Size, Images, Variants, SocialLinks
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

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']
    search_fields = ('name',)
    list_filter = ('name',)

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']
    search_fields = ('name','code')
    list_filter = ('name','code')


class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class SocialLinksInline(admin.TabularInline):
    model=SocialLinks
    readonly_fields=('id',)
    extra=1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status','image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    actions = ['make_published','make_unpublished','make_availabel','make_unavailabel']
    inlines = [ProductImageInline,ProductVariantsInline,SocialLinksInline]
    prepopulated_fields = {'slug': ('title',)}

    def make_published(modeladmin, request, queryset):
        queryset.update(status='True')
    make_published.short_description = "Make Product Visible To User"
    

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(status='False')
    make_unpublished.short_description = "Hide Product From User"
    
    def make_availabel(modeladmin, request, queryset):
        queryset.update(stocks='In-Stock')
    make_availabel.short_description = "Mark Products As In-Stocks"
    

    def make_unavailabel(modeladmin, request, queryset):
        queryset.update(stocks='Out-Of-Stock')
    make_unavailabel.short_description = "Mark Products As Out-Of-Stocks"

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','image_tag']

@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']

admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Category, CategoryAdmin)