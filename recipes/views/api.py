from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from tag.models import Tag
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from ..models import Recipe
from ..serialirzers import RecipeSerializer, TagSerializer

class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 1

class RecipeAPIV2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    

class RecipeAPIV2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)

        return recipe



    def get(self, request, pk):
        recipe = self.get_recipe(pk)

        serializer = RecipeSerializer(instance=recipe, many=False, context={'request': request})
        return Response(serializer.data)
        

    
    def patch(self, request, pk):
        recipe = self.get_recipe(pk)

        serializer = RecipeSerializer(instance=recipe,data=request.data ,many=False, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self,request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        


        




@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False, context={'request': request})
    return Response(serializer.data)