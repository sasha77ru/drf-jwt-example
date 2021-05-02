from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from myapi.core import views
from myapi.core.mytoken import MyTokenObtainPairView
from myapi.core.mytoken import MyTokenRefreshView

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
