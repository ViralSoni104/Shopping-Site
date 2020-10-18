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
    Member_Profile_Alternative_Text = models.CharField(blank=True,max_length=255)
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
    home_page_title = models.CharField(max_length=255,blank=True)
    account_page_title = models.CharField(max_length=255,blank=True)
    forget_page_title = models.CharField(max_length=255,blank=True)
    forget_comfirm_page_title = models.CharField(max_length=255,blank=True)
    change_password_page_title = models.CharField(max_length=255,blank=True)
    about_page_title = models.CharField(max_length=255,blank=True)
    contact_page_title = models.CharField(max_length=255,blank=True)
    faq_page_title = models.CharField(max_length=255,blank=True)
    error_404_page_title = models.CharField(max_length=255,blank=True)
    favourite_list_page_title = models.CharField(max_length=255,blank=True)
    home_page_meta_description=models.TextField(null=True,blank=True)
    home_page_meta_keywords=models.TextField(null=True,blank=True)
    about_page_meta_description=models.TextField(null=True,blank=True)
    about_page_meta_keywords=models.TextField(null=True,blank=True)
    contact_page_meta_description=models.TextField(null=True,blank=True)
    contact_page_meta_keywords=models.TextField(null=True,blank=True)
    faq_page_meta_description=models.TextField(null=True,blank=True)
    faq_page_meta_keywords=models.TextField(null=True,blank=True)
    Home_Page_Banner = models.ImageField(blank=True,upload_to='img/')
    Home_Page_Banner_Alternative_Text = models.CharField(blank=True,max_length=255)
    Home_Page_Small_Text = models.CharField(blank=True,max_length=255)
    Home_Page_Big_Text = models.CharField(blank=True,max_length=255)
    FaceBook_Account = models.CharField(blank=True,max_length=255)
    Twitter_Account = models.CharField(blank=True,max_length=255)
    Instagram_Account = models.CharField(blank=True,max_length=255)
    Linkedin_Account = models.CharField(blank=True,max_length=255)
    Address = models.CharField(blank=True,max_length=255)
    Contact_No_1 = models.CharField(blank=True,max_length=255)
    Contact_No_2 = models.CharField(blank=True,max_length=255)
    Email = models.EmailField(blank=True,max_length=255)
    Short_About_Us = models.TextField(blank=True)
    About_Us_Image = models.ImageField(blank=True,upload_to='img/')
    About_Us_Image_Alternative_Text = models.CharField(blank=True,max_length=255)
    About_Us = RichTextUploadingField()
    Our_Mission_Image = models.ImageField(blank=True,upload_to='img/')
    Our_Mission_Image_Alternative_Text = models.CharField(blank=True,max_length=255)
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

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    position_number = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    status=models.CharField(max_length=10, choices=STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question