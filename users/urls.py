from django.urls import path, include
from . views import SignUpView, LoginAPIView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
