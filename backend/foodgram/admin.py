from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Ingredient, Tag, Recipe, RecipeTags,
    RecipeIngredients, ShoppingList, Subscription, Favorites)
from users.models import Users

#Модель пользователи
class UsersAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'access')
    search_fields = ('name', 'email')
    list_filter = ('access',)

# Модель Ингридиент
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'unit')
    search_fields = ('name',)
    list_filter = ('name',)

# Модель Тег
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    #list_filter = ('color',)

# Модель Рецепт
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'pub_date', 'favorites')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    fields = ('name', 'author', 'picture', 'text', 'cooking_time')
    # fieldsets = (None,
    #              {'fields': ('pk', 'name', 'author', 'pub_date')}
    # )
    #     ('Advanced options', {
    #
    #         'fields': ('registration_required', 'template_name'),
    #     }),
    # )

    def favorites(self, obj):
        return obj.selected_users.count()
        #return '100'

# Модель Теги рецептов
class RecipeTagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    search_fields = ('recipe',)
    list_filter = ('tag',)

# Модель Ингридиенты рецептов
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'number')
    search_fields = ('recipe',)
    list_filter = ('ingredient',)

# Модель Список покупок
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)

# Модель Подписки
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    #list_filter = ('author',)

# Модель Избранное
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)

admin.site.register(Users, UsersAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTags, RecipeTagsAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Favorites, FavoritesAdmin)
# Register your models here.
