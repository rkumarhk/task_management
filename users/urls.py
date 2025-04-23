from django.urls import path, include
from . views import SignUpView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
]
