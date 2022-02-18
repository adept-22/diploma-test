from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.shortcuts import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

PAGINATOR_PAGE_SIZE = 6


from foodgram.models import Ingredient, Tag, Recipe, Subscription, Favorites, RecipeIngredients, ShoppingList
from users.models import Users
from .serializers import (IngredientSerializer, TagSerializer, ViewRecipesSerializer,
                          CreateOrСhangeRecipeSerializer, SubscriptionSerializer, FavouriteSerializer)
from .permissions import RecipePermission

#Вьюсет ингридиентов
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None

#Вьюсет тегов
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

#Вьюсет рецептов
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    #serializer_class = RecipeSerializer
    permission_classes = (RecipePermission, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewRecipesSerializer
        return CreateOrСhangeRecipeSerializer

    # def get_serializer_context(self):
    #
    #     context = super(RecipeViewSet, self).get_serializer_context()
    #     context.update({"request": self.request})
    #     return context

#Вьюсет подписок
# class SubscriptionViewSet(viewsets.ModelViewSet):
#     serializer_class = SubscriptionSerializer
#
#     def get_queryset(self):
#         user = Users.objects.get(username=self.request.user)
#         return user.following.all()

#APIView подписок
class SubscriptionViewSet(APIView):

    def get(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = PAGINATOR_PAGE_SIZE
        page = paginator.paginate_queryset(subscriptions, request)
        serializer = SubscriptionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


#APIView избранных рецептов
class FavouriteViewSet(APIView):
    #permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        user = request.user
        if not Recipe.objects.filter(id=id).exists():
            return Response(
                f'Рецепт с id {id} не найден!',
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = Recipe.objects.get(id=id)
        if Favorites.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                f'Рецепт с id {id} уже добавлен в избранное',
                status=status.HTTP_400_BAD_REQUEST)
        Favorites.objects.create(user=user, recipe=recipe)
        serializer = FavouriteSerializer(recipe)
        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        user = request.user
        if not Recipe.objects.filter(id=id).exists():
            return Response(
                f'Рецепт с id {id} не найден!',
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = Recipe.objects.get(id=id)
        #favorite_obj = get_object_or_404(Favorites, user=user, recipe=recipe)
        #if not favorite_obj:
        if not Favorites.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                f'Рецепт с id {id} не был в избранном',
                status=status.HTTP_400_BAD_REQUEST)
        favorites = Favorites.objects.get(user=user, recipe=recipe)
        favorites.delete()
        return Response(
            f'Рецепт с id {id} удален из избранного', status=status.HTTP_204_NO_CONTENT)

#APIView списка покупок
class ShoppingCartViewSet(APIView):
    # permission_classes = (IsAuthenticated, )

    def post(self, request, id):
        user = request.user
        if not Recipe.objects.filter(id=id).exists():
            return Response(
                f'Рецепт с id {id} не найден!',
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = Recipe.objects.get(id=id)
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
        if not Recipe.objects.filter(id=id).exists():
            return Response(
                f'Рецепт с id {id} не найден!',
                status=status.HTTP_404_NOT_FOUND
            )
        recipe = Recipe.objects.get(id=id)
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

#APIView выгрузки ингридиентов списка покупок
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