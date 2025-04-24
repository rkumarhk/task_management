from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .serializers import ProjectListSerializer, ProjectCreateSerializer
from .models import Project


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
        
    