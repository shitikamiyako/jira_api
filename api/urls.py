from django.urls import path, include
from rest_framework import routers

from .views import csrf, TokenObtainView, TaskViewSet, CategoryViewSet, ListUserView, LoginUserView, ProfileViewSet, \
    CreateUserView, refresh_get, TokenRefresh, LogoutView

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('csrf/create', csrf),
    path('jwtcookie/create', TokenObtainView.as_view(), name='jwtcreate'),
    path('jwtcookie/refresh', refresh_get),
    path('jwtcookie/newtoken', TokenRefresh.as_view(), name='jwtrefresh'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('users/', ListUserView.as_view(), name='users'),
    path('loginuser/', LoginUserView.as_view(), name='loginuser'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
