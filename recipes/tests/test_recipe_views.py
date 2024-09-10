from django.test import TestCase
from django.urls import reverse, resolve

from recipes import views

class RecipeViewsTest(TestCase):
    
    def test_recipe_recipe_detail_view_fuction_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
    
    
    
        