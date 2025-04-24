from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound, ValidationError, APIException
from django.db import transaction
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

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
        
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")
        


class LoginAPIView(APIView):
    permission_classes = []

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