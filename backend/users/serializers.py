from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
#from rest_framework.validators import UniqueTogetherValidator

#from api.models import Recipe
from .models import Users


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = Users
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

# Сериализатор djoser который обрабатывает users/
class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(method_name='get_subscriptions_users')

    class Meta:
        model = Users
        fields = (
            'email','id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_subscriptions_users(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and user.following.filter(author=obj).exists())