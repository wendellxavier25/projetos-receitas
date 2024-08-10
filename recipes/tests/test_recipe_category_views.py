from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views

class RecipeCategoryViewsTest(TestCase):

     def test_recipe_category_view_fuction_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)