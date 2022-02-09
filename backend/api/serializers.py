from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from foodgram.models import Ingredient, Tag, RecipeIngredients, Recipe, Subscription, ShoppingList, Favorites
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

#Сериализатор для GET-запросов рецептов
class ViewRecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(method_name='get_recipe_ingredient')
    picture = serializers.ImageField(max_length=None, required=True, allow_empty_file=False)#, #use_url=True)
    is_favorited = serializers.SerializerMethodField(method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(method_name='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart',
                  'name', 'picture', 'text', 'cooking_time')

    def get_recipe_ingredient(self, obj):
        ingredients = obj.ingredient_list.all()
        return RecipeIngredientsSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorites.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(recipe=obj, user=request.user).exists()

#Сериализатор для добавления рецептов
class IngredientsToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    number = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'number')

#Сериализатор для POST и PATCH-запросов рецептов
class CreateOrСhangeRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsToRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    picture = Base64ImageField(max_length=None)#, use_url=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'picture', 'name',
                  'text', 'cooking_time') #'author

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        cooking_time = self.initial_data.get('cooking_time')
        if not ingredients:
            raise serializers.ValidationError(
                'Отсутствуют ингредиенты'
            )
        ingredient_id = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredient_id:
                raise serializers.ValidationError(
                    'Повторяющиеся ингредиенты'
                )
            ingredient_id.append(ingredient['id'])
            if ingredient['number'] < 1:
                raise serializers.ValidationError(
                    'Недопустимое количество ингредиента'
                )
        if not tags:
            raise serializers.ValidationError(
                'Отсутствуют теги'
            )
        tags_id = []
        for tag in tags:
            if tag in tags_id:
                raise serializers.ValidationError(
                    'Повторяющиеся теги'
                )
            tags_id.append(tag)
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Недопустимое время приготовления'
            )
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=author,
            **validated_data
        )
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                number=ingredient['number']
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.image = validated_data.pop('picture')
        instance.cooking_time = validated_data.pop('cooking_time')
        RecipeIngredients.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=instance,
                ingredient=ingredient['ingredient'],
                number=ingredient['number']
            )
        instance.tags.set(tags)
        return instance

    def to_representation(self, instance):
        return ViewRecipesSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

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

#Сериализатор избранных рецептов
class FavouriteSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(max_length=None, required=True, allow_empty_file=False, use_url=True)

    class Meta:
        model = Recipe
        #fields = ('id', 'name', 'image', 'cooking_time')
        fields = ('id', 'name', 'picture', 'cooking_time')


#Подумать
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=ShoppingCart.objects.all(),
        #         fields=('user', 'recipe'),
        #         message='ShoppingCartObject already exists',
        #     ),
        # ]