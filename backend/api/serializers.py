from rest_framework import serializers

from foodgram.models import Ingredient, Tag, RecipeIngredients, Recipe, Subscription
from users.serializers import CustomUserSerializer

#Сериализатр ингридиенты
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'unit')

#Сериализатр теги
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

#Сериализатор ингредиентов рецепта
class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'number')

#Сериализатор рецепты
class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    #ingredients = IngredientSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField(method_name='get_recipe_ingredient')

    class Meta:
        model = Recipe
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        #           'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'text', 'cooking_time')


    def get_recipe_ingredient(self, obj):
        ingredients = obj.ingredient_list.all()
        return RecipeIngredientsSerializer(ingredients, many=True).data

#Сериализатор подписки
class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(method_name='get_subscriptions_users')
    #recipes = serializers.SerializerMethodField()
    #recipes_count = serializers.SerializerMethodField(method_name='get_recipes_count')

    class Meta:
        model = Subscription
        #fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        #fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes_count')
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_subscriptions_users(self, obj):
        return True


#переделать
    # def get_recipes(self, obj):
    #     request = self.context.get("request")
    #     limit = request.GET.get("recipes_limit")
    #     queryset = Recipe.objects.filter(author=obj.author)
    #     if limit:
    #         queryset = queryset[: int(limit)]
    #     return CropRecipeSerializer(queryset, many=True).data

#подумать как переделать в релейтед фил
    def get_recipes_count(self, obj):
        print('*******')
        print(obj)
        print(author=obj.author)
        return 1
        #return Recipe.objects.filter(author=obj.author).count()