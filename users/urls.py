from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import  UserLogin , RegisterView

router = DefaultRouter()

urlpatterns = router.urls
urlpatterns += [
    path('login/', UserLogin.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register')
]