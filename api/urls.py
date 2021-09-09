from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet, CategoryViewSet, ListUserView, LoginUserView, ProfileViewSet, CreateUserView

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('category', CategoryViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreateUserView.as_view(), name='create'),
    path('users/', ListUserView.as_view(), name='users'),
    path('loginuser/', LoginUserView.as_view(), name='loginuser')
]