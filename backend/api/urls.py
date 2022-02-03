from rest_framework.routers import DefaultRouter
from django.urls import include, path
#from rest_framework import routers

from .views import IngredientViewSet, TagViewSet, RecipeViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users/subscriptions', SubscriptionViewSet, basename='subscription')
# #router.register(
#     r'recipes/(?P<recipe_id>\d+)/shopping_cart',
#     ChangeShoppingListViewSet,
#     basename="shopping_cart",
# )

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include("djoser.urls")),
    #re_path(r"^auth/", include("djoser.urls.authtoken")),
]

