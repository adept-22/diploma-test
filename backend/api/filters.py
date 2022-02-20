# from django_filters.rest_framework import FilterSet, filters
#
# class RecipeFilter(FilterSet):
#     tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
#     #is_favorited = filters.BooleanFilter(method='filter_is_favorited')
#     # is_in_shopping_cart = filters.BooleanFilter(
#     #     method='filter_is_in_shopping_cart'
#     # )
#
#     class Meta:
#         model = Recipe
#         #fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
#         fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

import django_filters as filters

from foodgram.models import Ingredient, Tag, Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited',
            'is_in_shopping_cart'
        )

    def filter_is_favorited(self, queryset, *args):
        return queryset.favourites(self.request.user)

    def filter_is_in_shopping_cart(self, queryset, *args):
        return queryset.purchases(self.request.user)