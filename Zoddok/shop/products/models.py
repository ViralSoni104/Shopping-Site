from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import mptt
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.templatetags.mptt_tags import cache_tree_children
from accounts.models import CustomUser

class Category(MPTTModel):
    STATUS=(
        ('True','True'),
        ('False','False'),
    )
    FEATURE=(
        ('Yes','Yes'),
        ('No','No'),
    )
    title = models.CharField(max_length=50)
    description=models.CharField(max_length=255,unique=True)
    meta_description=models.TextField(null=True,blank=True)
    meta_keywords=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    feature_to_home_page=models.CharField(max_length=10,choices=FEATURE,default='No')
    image=models.ImageField(blank=True,upload_to='img/')
    image_alternative_text = models.CharField(blank=True,max_length=255)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',db_index=True)
    slug = models.SlugField(null=False,unique=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name_plural = 'categories'
    
    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
            slugs = []
            for i in range(len(ancestors)):
                slugs.append('/'.join(ancestors[:i+1]))
            return slugs

    def __str__(self):
        return self.title
    
    def get_child_count(self):
        if self._mpttfield('right') is None:
            return 0
        else:
            childs=self.get_children()
            count=0
            for n in childs:
                count+=1
            return count
            #return ( self._mpttfield('right') - self._mpttfield('left') - 1 ) // 2 


    def get_absolute_url(self):
        slugs=''
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [ i.slug for i in ancestors]
            for i in range(len(ancestors)):
                if i==0:
                    slugs+=ancestors[i]
                else:
                    slugs+='/'
                    slugs+=ancestors[i]
            return reverse('category', kwargs={'slug': slugs})

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    STOCKS = (
        ('In-Stock', 'In-Stock'),
        ('Out-Of-Stock', 'Out-Of-Stock'),
    )
    FEATURE=(
        ('Yes','Yes'),
        ('No','No'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    title = models.CharField(max_length=150)
    #keywords = models.CharField(max_length=255)
    meta_description=models.TextField(null=True,blank=True)
    meta_keywords=models.TextField(null=True,blank=True)
    description = models.TextField()
    image=models.ImageField(upload_to='img/',null=False)
    image_alternative_text = models.CharField(blank=True,max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    stocks=models.CharField(max_length=12,choices=STOCKS, default='In-Stock')
    detail=RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    feature_to_home_page=models.CharField(max_length=10,choices=FEATURE,default='No')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(CustomUser,related_name='product_favorite',blank=True)

    def __str__(self):
        return self.title

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='img/')
    image_alternative_text = models.CharField(blank=True,max_length=255)
    def __str__(self):
        return self.title

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    #quantity = models.IntegerField(default=1)
    #price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

class SocialLinks(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    link=models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.name


