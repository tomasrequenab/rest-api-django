from calendar import c
from rest_framework import serializers

from core.models import Tag, Ingrendient, Recipe


class TagSerializer(serializers.ModelSerializer):
    '''Serializer for tag objects'''

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    '''Serializer for ingredient objects'''

    class Meta:
        model = Ingrendient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingrendient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes',
            'price', 'link'
        )
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)



class RecipeImageSerializer(serializers.ModelSerializer):
    '''Serializer for uploading images to recipes '''
    
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)