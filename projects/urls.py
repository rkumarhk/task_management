from django.urls import path, include
from .views import ProjectApiView, TaskApiView, CommentApiView
from users.swagger import schema_view

urlpatterns = [
    path('projects/', ProjectApiView.as_view(), name='project-view'),
    path('projects/<int:pk>/', ProjectApiView.as_view(), name='project-detail'),
    path('task/', TaskApiView.as_view(), name='task-view'),
    path('task/<int:pk>/', TaskApiView.as_view(), name='task-detail'),
    path('comment/', CommentApiView.as_view(), name='comment-view'),
    path('comment/<int:pk>/', CommentApiView.as_view(), name='comment-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
