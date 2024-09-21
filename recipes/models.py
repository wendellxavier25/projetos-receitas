from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from tag.models import Tag
from django.utils.translation import gettext_lazy as _
import os
from django.conf import settings
from PIL import Image
from collections import defaultdict
from django.forms import ValidationError
from django.db.models.functions import Concat
from django.db.models import F, Value


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).annotate(
            author_full_name=Concat(
                F('authorr__first_name'), Value(' '),
                F('authorr__last_name'), Value('('),
                F('authorr__username'), Value(')'),
            )).order_by('-id')

class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.CharField(max_length=150, verbose_name=_("Description"))
    slug = models.SlugField(unique=True,)
    preparation_time = models.IntegerField(verbose_name=_("Preparation time"))
    preparation_time_unit = models.CharField(max_length=65, verbose_name=_("Preparation time unit"))
    servings = models.IntegerField(verbose_name=_("Servings"))
    servings_unit = models.CharField(max_length=65, verbose_name=_("Servings unit"))
    preparation_steps = models.TextField(verbose_name=_("Preparation steps"))
    preparation_steps_is_html = models.BooleanField(default=False, verbose_name=_("Preparation steps is html"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    update_at = models.DateField(auto_now=True, verbose_name=_("Update at"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is published"))
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', verbose_name=_("Cover"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_("Category"))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Author"))
    tags = models.ManyToManyField(Tag, blank=True, default='', verbose_name=_("Tags"))
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))
    
    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_heigth = image_pillow.size

        if original_width < new_width:
            image_pillow.close()
            return
        
        new_heigth = round(new_width * original_heigth) / original_width

        new_image = image_pillow.resize((new_width, new_heigth), Image.LANCZOS)

        new_image.save(image_full_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):

        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 800)
            except FileNotFoundError:
                ...

        return saved
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(title__eixact=self.title).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append('Found recipes with the same title')

        if error_messages:
            raise ValidationError(error_messages)
    
