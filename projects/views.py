from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from .serializers import ProjectListSerializer, ProjectCreateSerializer, \
    TaskCreateSerializer, TaskListSerializer, CommentCreateSerializer
from .models import Project, Task, Comment
# from users.pagination import CustomPagination
from rest_framework.pagination import PageNumberPagination

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class ProjectApiView(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [JWTAuthentication]
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    pagination_class = CustomPagination

    print("Authorization Header:")

    def get_queryset(self):
        """
        Filter the queryset based on query parameters.
        """
        queryset = self.queryset
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        created_by = self.request.query_params.get('created_by')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if created_by:
            queryset = queryset.filter(created_by_id=created_by)

        

        return queryset


    def get_paginator(self):
        """
        Create and return a single instance of the paginator.
        """
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Paginate the queryset using the paginator instance.
        """
        paginator = self.get_paginator()
        return paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated response using the paginator instance.
        """
        paginator = self.get_paginator()
        return paginator.get_paginated_response(data)



    def get_object(self, pk):
        try:
            return self.queryset.filter(id=pk).first()
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

    @method_decorator(cache_page(60 * 15))
    def get(self, request, pk=None):
        # try:
            print("Authorization Header:", request.headers.get('Authorization'))
            # Check if the user is authenticated
            if request.user.is_authenticated:
                return Response({"message": "Welcome Back!"}, status=status.HTTP_200_OK)
            if pk:
                project = self.get_object(pk)
                serializer = ProjectListSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                queryset = self.get_queryset().all()
                page = self.paginate_queryset(queryset) 

                if page is not None:
                    serializer = ProjectListSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
        
                    # If pagination is not used, return all results
                serializer = ProjectListSerializer(self.queryset.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     print("Authorization Header:", request.headers.get('Authorization'))
        #     # Check if the user is authenticated
        #     if request.user.is_authenticated:
        #         return Response({"message": "Welcome Back!"}, status=status.HTTP_200_OK)
        #     raise APIException(f"An error occurred here: {str(e)}")
        
    
    def post(self, request):
        try:
            user = request.user

            # if user.role != 'projectmanager':
            #     return Response({
            #         "message": "You do not have permission to create a project"
            #     }, status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            serializer = ProjectCreateSerializer(data=data)
            if serializer.is_valid():
                project = serializer.save(created_by=user)
                return Response({"message": "Project created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            raise APIException(f"An error occurred: {str(e)}")
        
        
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "Project ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            

            project = self.get_object(pk)

            # if project.created_by != request.user:
            #     return Response({
            #         "message": "You do not have permission to update this project"
            #     }, status=status.HTTP_403_FORBIDDEN)
            

            serializer = ProjectCreateSerializer(project, data=request.data, partial=True)
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_project = serializer.save()
                    return Response({
                        "message": "Project updated successfully",
                        "data": ProjectListSerializer(updated_project).data
                    }, status=status.HTTP_200_OK)
                    
            return Response({
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            return Response({
                "message": "Project not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    def delete(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "Project ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            project = self.get_object(pk)
            
            # Check if user has permission to delete
            # user = request.user
            # if user.role not in ['superadmin', 'admin', 'projectmanager']:
            #     return Response({
            #         "message": "You do not have permission to delete this project"
            #     }, status=status.HTTP_403_FORBIDDEN)

            with transaction.atomic():
                project.delete()
                return Response({
                    "message": "Project deleted successfully"
                }, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response({
                "message": "Project not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")

        
    


class TaskApiView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    pagination_class = CustomPagination

    
    def get_queryset(self):
        """
        Filter the queryset based on query parameters.
        """
        queryset = self.queryset
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        created_by = self.request.query_params.get('created_by')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        

        return queryset



    def get_paginator(self):
        """
        Create and return a single instance of the paginator.
        """
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Paginate the queryset using the paginator instance.
        """
        paginator = self.get_paginator()
        return paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated response using the paginator instance.
        """
        paginator = self.get_paginator()
        return paginator.get_paginated_response(data)



    def get_object(self, pk):
        try:
            return self.queryset.filter(id=pk).first()
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

    @method_decorator(cache_page(60 * 15))
    def get(self, request, pk=None):
        try:
            if pk:
                tasks = self.get_object(pk)
                serializer = TaskCreateSerializer(tasks)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # projects = Project.objects.all()
                queryset = self.get_queryset().all()
                page = self.paginate_queryset(queryset)

                if page is not None:
                    serializer = TaskListSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
        
                    # If pagination is not used, return all results
                serializer = TaskListSerializer(self.queryset.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    
    def post(self, request):
        try:
            data = request.data
            serializer = TaskCreateSerializer(data=data)
            if serializer.is_valid():
                task = serializer.save(created_by_id=1)
                return Response({"message": "Task created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "Task ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            task = self.get_object(pk)
            serializer = TaskCreateSerializer(task, data=request.data, partial=True)
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_task = serializer.save()
                    return Response({
                        "message": "Task updated successfully",
                        "data": TaskListSerializer(updated_task).data
                    }, status=status.HTTP_200_OK)
                    
            return Response({
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Task.DoesNotExist:
            return Response({
                "message": "Project not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    def delete(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "Task ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            task = self.get_object(pk)
            
            # Check if user has permission to delete
            user = request.user
            # if task.created_by != user or user.role not in ['superadmin', 'admin', 'projectmanager']:
            #     return Response({
            #         "message": "You do not have permission to delete this task"
            #     }, status=status.HTTP_403_FORBIDDEN)

            
            task.is_active = False
            task.is_delete = True
            task.save()
            return Response({
                "message": "Project deleted successfully"
            }, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            return Response({
                "message": "Task not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")

        
        
    

class CommentApiView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Filter the queryset based on query parameters.
        """
        queryset = self.queryset

        status = self.request.query_params.get('status')
        q = self.request.query_params.get('q')
        priority = self.request.query_params.get('priority')
        created_by = self.request.query_params.get('created_by')

        if status:
            queryset = queryset.filter(status=status)
        if q:
            queryset = queryset.filter(content__icontains=q)
        if priority:
            queryset = queryset.filter(priority=priority)
        if created_by:
            queryset = queryset.filter(author_id=created_by)

        return queryset

    def get_paginator(self):
        """
        Create and return a single instance of the paginator.
        """
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Paginate the queryset using the paginator instance.
        """
        paginator = self.get_paginator()
        return paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated response using the paginator instance.
        """
        paginator = self.get_paginator()
        return paginator.get_paginated_response(data)



    def get_object(self, pk):
        try:
            return self.queryset.filter(id=pk).first()
        except Comment.DoesNotExist:
            raise NotFound(detail="Comment not found")

    @method_decorator(cache_page(60 * 15))
    def get(self, request, pk=None):
        try:
            if pk:
                comments = self.get_object(pk)
                serializer = CommentCreateSerializer(comments)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                queryset = self.get_queryset().all()
                page = self.paginate_queryset(queryset)
                if page is not None:    
                    serializer = CommentCreateSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
        
                    # If pagination is not used, return all results
                serializer = CommentCreateSerializer(self.queryset.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    
    def post(self, request):
        try:
            data = request.data
            serializer = CommentCreateSerializer(data=data)
            if serializer.is_valid():
                comment = serializer.save(author=request.user)
                return Response({"message": "Comment created successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    
    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "Comment ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            comment = self.get_object(pk)
            serializer = TaskCreateSerializer(comment, data=request.data, partial=True)
            
            if serializer.is_valid():
                with transaction.atomic():
                    updated_comment = serializer.save()
                    return Response({
                        "message": "Comment updated successfully",
                        "data": CommentCreateSerializer(updated_comment).data
                    }, status=status.HTTP_200_OK)
                    
            return Response({
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Comment.DoesNotExist:
            return Response({
                "message": "Comment not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    def delete(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "Comment ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            comment = self.get_object(pk)
            
            # Check if user has permission to delete
            user = request.user
            # if user.job_role not in ['superadmin', 'admin', 'projectmanager']:
            #     return Response({
            #         "message": "You do not have permission to delete this project"
            #     }, status=status.HTTP_403_FORBIDDEN)

            with transaction.atomic():
                comment.is_active = False
                comment.is_delete = True
                comment.save()
                return Response({
                    "message": "Comment deleted successfully"
                }, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return Response({
                "message": "Comment not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    