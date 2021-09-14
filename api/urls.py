from django.urls import path, include
from rest_framework import routers

from .views import TokenObtainView, TaskViewSet, CategoryViewSet, ListUserView, LoginUserView, ProfileViewSet, \
    CreateUserView, refresh_get

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get/jwt/create', TokenObtainView.as_view(), name='jwtcreate'),
    path('get/jwt/refresh', refresh_get),
    path('get/jwt/newtoken', TokenObtainView.as_view(), name='jwtrefresh'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('users/', ListUserView.as_view(), name='users'),
    path('loginuser/', LoginUserView.as_view(), name='loginuser')
]
