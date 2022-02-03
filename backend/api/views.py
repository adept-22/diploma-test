from rest_framework import viewsets

from foodgram.models import Ingredient, Tag, Recipe, Subscription
from users.models import Users
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, SubscriptionSerializer

#Вьюсет ингридиентов
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

#Вьюсет тегов
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

#Вьюсет рецептов
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

#Вьюсет подписок
class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = Users.objects.get(username=self.request.user)
        return user.following.all()
