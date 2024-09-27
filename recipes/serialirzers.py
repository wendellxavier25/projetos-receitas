from rest_framework import serializers
from django.contrib.auth.models import User
from tag.models import Tag
from .models import Recipe

class TagSerializer(serializers.ModelSerializer):
   class Meta:
       model = Tag
       fields = ['id', 'name', 'slug']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'author', 'tags', 'public',
                   'preparation', 'tag_objects', 'tag_links']

   
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name='any_method_name')
    category = serializers.StringRelatedField(read_only=True)
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(many=True, source='tags', read_only=True, view_name='recipes:recipe_api_v2_tag')



    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        
        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["Posso", "ter", "mais de um erro"],
                    "description": ["Posso", "ter", "mais de um erro"],
                }
            )
        
        return super_validate
    

    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')
        
        return title