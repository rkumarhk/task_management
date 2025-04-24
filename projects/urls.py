from django.urls import path, include
from .views import ProjectApiView

urlpatterns = [
    path('', ProjectApiView.as_view(), name='project-view'),
    path('<int:pk>/', ProjectApiView.as_view(), name='project-detail'),
]
