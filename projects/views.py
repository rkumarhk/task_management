from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .serializers import ProjectListSerializer, ProjectCreateSerializer, \
    TaskCreateSerializer, TaskListSerializer, CommentCreateSerializer
from .models import Project, Task, Comment


class ProjectApiView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def get_object(self, pk):
        try:
            return self.queryset.filter(id=pk).first()
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

    
    def get(self, request, pk=None):
        try:
            if pk:
                project = self.get_object(pk)
                serializer = ProjectListSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # projects = Project.objects.all()
                serializer = ProjectListSerializer(self.queryset.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    
    def post(self, request):
        try:
            data = request.data
            serializer = ProjectCreateSerializer(data=data)
            if serializer.is_valid():
                project = serializer.save()
                return Response({"message": "Project created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    


class TaskApiView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def get_object(self, pk):
        try:
            return self.queryset.filter(id=pk).first()
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

    
    def get(self, request, pk=None):
        try:
            if pk:
                tasks = self.get_object(pk)
                serializer = TaskCreateSerializer(tasks)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # projects = Project.objects.all()
                serializer = TaskListSerializer(self.queryset.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    
    def post(self, request):
        try:
            data = request.data
            serializer = TaskCreateSerializer(data=data)
            if serializer.is_valid():
                task = serializer.save()
                return Response({"message": "Task created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    

class CommentApiView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def get_object(self, pk):
        try:
            return self.queryset.filter(id=pk).first()
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

    
    def get(self, request, pk=None):
        try:
            if pk:
                comments = self.get_object(pk)
                serializer = CommentCreateSerializer(comments)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = CommentCreateSerializer(self.queryset.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    
    def post(self, request):
        try:
            data = request.data
            serializer = CommentCreateSerializer(data=data)
            if serializer.is_valid():
                comment = serializer.save()
                return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    