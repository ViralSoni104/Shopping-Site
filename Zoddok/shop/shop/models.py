from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class Contact(models.Model):
    contact_name=models.CharField(max_length=50)
    contact_email=models.EmailField(max_length=255)
    message=models.TextField()
    contacted_on=models.DateTimeField(null=True,blank=True,auto_now_add=True)

class Team(models.Model):
    Member_Name = models.CharField(blank=False,max_length=70)
    Member_Position = models.CharField(blank=False,max_length=100)
    Member_Profile = models.ImageField(blank=False,upload_to="img/")
    Member_FaceBook_Account = models.CharField(blank=True,max_length=255)
    Member_Twitter_Account = models.CharField(blank=True,max_length=255)
    Member_Instagram_Account = models.CharField(blank=True,max_length=255)
    Member_Linkdin_Account = models.CharField(blank=True,max_length=255)

    def image_tag(self):
        if self.Member_Profile is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Member_Profile.url))
        else:
            return ""
    
    def __str__(self):
        return self.Member_Name


class SiteSetting(models.Model):
    Fav_Icon = models.ImageField(upload_to='img/')
    Site_Logo = models.ImageField(upload_to='img/')
    Home_Page_Banner = models.ImageField(blank=True,upload_to='img/')
    FaceBook_Account = models.CharField(blank=True,max_length=255)
    Twitter_Account = models.CharField(blank=True,max_length=255)
    Instagram_Account = models.CharField(blank=True,max_length=255)
    Linkedin_Account = models.CharField(blank=True,max_length=255)
    Contact_No_1 = models.CharField(blank=True,max_length=255)
    Contact_No_2 = models.CharField(blank=True,max_length=255)
    Email = models.EmailField(blank=True,max_length=255)
    Short_About_Us = models.TextField(blank=True)
    About_Us = RichTextUploadingField()
    Our_Mission = RichTextUploadingField()

    def fav_icon_image_tag(self):
        if self.Fav_Icon is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Fav_Icon.url))
        else:
            return ""
    
    def logo_image_tag(self):
        if self.Site_Logo is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Site_Logo.url))
        else:
            return ""