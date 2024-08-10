from django.test import TestCase
from django.urls import reverse
from recipes import views


class RecipeSearchViewsTest(TestCase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = reverse(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        reponse = self.client.get(reverse('recipes:home'))
        self.assertEqual(reponse.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<teste>'
        response = self.client.get(url)
        self.assertIn('Search for &quot;&lt;teste&gt;&quot;', response.content.decode('utf-8'))
        
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'this is recipe one'
        title2 = 'this is recipe two'
        
        recipe1 = self.make_recipe(slug='one', title=title1, author_data={'username': 'one'})
        
        recipe2 = self.make_recipe(slug='one', title=title2, author_data={'username': 'two'})
        
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')
        
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])
        
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])