from django.shortcuts import render
from rest_framework.permissions import AllowAny
from djoser.views import UserViewSet
from .models import Users

# class CustomUserViewSet(UserViewSet):
#     queryset = Users.objects.all()
#     #serializer_class = CustomUserSerializer
#     #pagination_class = CustomPageNumberPaginator
#     #permission_classes = (AllowAny, )
#
#     def get_permission_classes(self, request):
#         print(request)
#         return AllowAny



