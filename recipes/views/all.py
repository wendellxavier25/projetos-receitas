import os
from django.shortcuts import render, get_object_or_404
from recipes.models import Recipe

def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    
    return render(request,'recipes/pages/recipe-view.html', {'is_detail_page': True, 'recipe': recipe,})


