from django.contrib import admin
from .forms import ContactForm
from .models import Contact, Team, SiteSetting, FAQ

class ContactAdmin(admin.ModelAdmin):
    model=Contact
    ordering=('-contacted_on',)
    list_display = ('contact_email','contact_name','message')
    list_filter = ('contacted_on',)
    search_fields = ('contact_name','contact_mail','message')

class TeamAdmin(admin.ModelAdmin):
    model=Team
    ordering=('Member_Name',)
    list_display = ('Member_Name','Member_Position','image_tag')
    list_filter = ('Member_Position',)
    readonly_fields = ('image_tag',)

class SiteAdmin(admin.ModelAdmin):
    model=SiteSetting
    list_display = ('logo_image_tag','fav_icon_image_tag','Contact_No_1','Email')
    
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','position_number','status']
    list_filter = ['status',]
    actions = ['make_published','make_unpublished']

    def make_published(modladmin, request, queryset):
        queryset.update(status='True')
    make_published.short_description = "Make FAQ Visible To User"
    

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(status='False')
    make_unpublished.short_description = "Hide FAQ From User"


admin.site.register(Contact,ContactAdmin)
admin.site.register(Team,TeamAdmin)
admin.site.register(SiteSetting,SiteAdmin)
admin.site.register(FAQ,FAQAdmin)