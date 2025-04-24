from django.urls import path, include
from . views import SignUpView, LoginAPIView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/<int:pk>/', SignUpView.as_view(), name='profile-detail'),
    path('login/', LoginAPIView.as_view(), name='login'),
    
]
