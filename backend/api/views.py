from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.shortcuts import HttpResponse


from foodgram.models import Ingredient, Tag, Recipe, Subscription, Favorites, RecipeIngredients, ShoppingList
from users.models import Users
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, SubscriptionSerializer, FavouriteSerializer

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

#APIView избранных рецептов
class FavouriteViewSet(APIView):
    #permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if Favorites.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Вы уже добавили рецепт в избранное',
                status=status.HTTP_400_BAD_REQUEST)
        Favorites.objects.create(user=user, recipe=recipe)
        serializer = FavouriteSerializer(recipe)
        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favorite_obj = get_object_or_404(Favorites, user=user, recipe=recipe)
        if not favorite_obj:
            return Response(
                'Рецепт не был в избранном',
                status=status.HTTP_400_BAD_REQUEST)
        favorite_obj.delete()
        return Response(
            'Удалено', status=status.HTTP_204_NO_CONTENT)

# class FavouriteViewSet(APIView):
#     #permission_classes = (IsAuthenticated, )
#
#     def post(self, request, id):
#         user = request.user
#         recipe = get_object_or_404(Recipe, id=id)
#         if Favorites.objects.filter(user=user, recipe=recipe).exists():
#             return Response(
#                 'Вы уже добавили рецепт в избранное',
#                 status=status.HTTP_400_BAD_REQUEST)
#         Favorites.objects.create(user=user, recipe=recipe)
#         serializer = FavouriteSerializer(recipe)
#         return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED)
#
#     def delete(self, request, id):
#         user = request.user
#         recipe = get_object_or_404(Recipe, id=id)
#         favorite_obj = get_object_or_404(Favorites, user=user, recipe=recipe)
#         if not favorite_obj:
#             return Response(
#                 'Рецепт не был в избранном',
#                 status=status.HTTP_400_BAD_REQUEST)
#         favorite_obj.delete()
#         return Response(
#             'Удалено', status=status.HTTP_204_NO_CONTENT)

class ShoppingCartViewSet(APIView):
    # permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Этот рецепт есть в списке покупок!',
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = FavouriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        if not ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Этого рецепта нет в списке покупок!',
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_list = ShoppingList.objects.get(user=user, recipe=recipe)
        shopping_list.delete()
        return Response(
            'Рецепт успешно удален из списка покупок!',
            status=status.HTTP_204_NO_CONTENT
        )


class DownloadShoppingCart(APIView):
    #permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        ingredients = RecipeIngredients.objects.filter(
                recipe__shopping_lists__user=user)\
                .values('ingredient__name', 'number', 'ingredient__unit')\
                .order_by('ingredient__name')
        cart = {}
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            number = ingredient['number']
            unit = ingredient['ingredient__unit']
            if name in cart:
                cart[name][0] += number
            else:
                cart[name] = [number, unit]
        cart_list = (f'***********************************\n'
                     f'Список покупок пользователя {user}\n'
                     f'***********************************\n'
        )
        for record in cart.keys():
            cart_list += f'{record} {str(cart[record][0])} {cart[record][1]}\n'
        response = HttpResponse(cart_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response