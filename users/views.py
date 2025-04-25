from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound, ValidationError, APIException
from django.db import transaction
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import login, authenticate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SignUpView(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")

    def post(self, request):
        try:
            with transaction.atomic():
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    def get(self, request, pk=None):
        try:
            if pk:
                user = self.get_object(pk)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # if not request.user.is_authenticated:
                #     return Response({
                #         "message": "You are not authenticated"
                #     }, status=status.HTTP_401_UNAUTHORIZED)
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        

    def put(self, request, pk=None):
        try:
            if not pk:
                return Response({
                    "message": "User ID is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            

            user = self.get_object(pk)
 
            if user != request.user:
                return Response({
                    "message": "You do not have permission to update this profile"
                }, status=status.HTTP_403_FORBIDDEN)
            

            serializer = UserSerializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_profile = serializer.save()
                return Response({
                    "message": "Profile updated successfully",
                    "data": UserSerializer(updated_profile).data
                }, status=status.HTTP_200_OK)
                    
            return Response({
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        
    def delete(self, request):
        try:
            user = request.user
            user.is_active = False
            # user.is_delete = True
            user.save()
            return Response({
                "message": "Profile deleted successfully"
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]


    @swagger_auto_schema(
        operation_description="User login API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description="User's email address"
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    description="User's password"
                )
            }
        ))
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                user = User.objects.get(email=email)
                if not user.check_password(password):
                    return Response({
                        'status': False,
                        'message': 'Invalid credentials',
                        'errors': {'non_field_errors': ['Invalid email or password']}
                    }, status=status.HTTP_400_BAD_REQUEST)
                elif user.account_status != 'active':
                    return Response({
                        'status': False,
                        'message': 'Account is not active',
                        'errors': {'non_field_errors': ['Account is not active']}
                    }, status=status.HTTP_400_BAD_REQUEST)

                authenticate_user = authenticate(username=email, password=password)
                if authenticate_user is not None:
                    login(request, authenticate_user)
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'status': True,
                    'message': 'Login successful',
                    'data': {
                        'token': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh)
                        },
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': False,
                'message': 'Invalid credentials',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)