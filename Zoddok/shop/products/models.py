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

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    FEATURE=(
        ('Yes','Yes'),
        ('No','No'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    meta_description=models.TextField(null=True,blank=True)
    meta_keywords=models.TextField(null=True,blank=True)
    product_title=models.CharField(max_length=255,default=None)
    product_link=models.TextField(default=None)
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    feature_to_home_page=models.CharField(max_length=10,choices=FEATURE,default='No')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(CustomUser,related_name='product_favorite',blank=True)

    def __str__(self):
        return self.product_link


    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})



