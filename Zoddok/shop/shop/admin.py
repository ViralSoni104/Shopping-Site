from django.contrib import admin
from .forms import ContactForm
from .models import Contact, Team, SiteSetting

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
    

admin.site.register(Contact,ContactAdmin)
admin.site.register(Team,TeamAdmin)
admin.site.register(SiteSetting,SiteAdmin)