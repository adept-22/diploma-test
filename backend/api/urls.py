from rest_framework.routers import DefaultRouter
from django.urls import include, path
#from rest_framework import routers

from .views import (IngredientViewSet, TagViewSet, RecipeViewSet,
                    SubscriptionViewSet, FavouriteViewSet, ShoppingCartViewSet,
                    DownloadShoppingCart, AddOrRemoveSubscriptionViewSet)

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
#router.register(r'users/subscriptions', SubscriptionViewSet, basename='subscription')
# #router.register(
#     r'recipes/(?P<recipe_id>\d+)/shopping_cart',
#     ChangeShoppingListViewSet,
#     basename="shopping_cart",
# )

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<int:id>/favorite/', FavouriteViewSet.as_view(), name='add_recipe_to_favorite'),
    #path('users/<int:id>/subscribe/', SubscriptionView.as_view(), name='subscribe'),#?

    path('users/subscriptions/', SubscriptionViewSet.as_view(), name='subscription_list'),
    path('users/<int:id>/subscribe/', AddOrRemoveSubscriptionViewSet.as_view(), name='add_remove_subscription'),

    path('recipes/<int:id>/shopping_cart/', ShoppingCartViewSet.as_view(), name='shopping_cart'),
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view(), name='dowload_shopping_cart'),
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    #re_path(r"^auth/", include("djoser.urls.authtoken")),
]

