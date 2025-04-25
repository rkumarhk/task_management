from .models import User
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'account_status', 'job_role']
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value.lower()
    

    def validate_phone(self, value):
        phone = re.sub(r'[\s\-\(\)]', '', value)
    
        # Check if phone number contains only digits and has length of 10
        if not re.match(r'^\d{10}$', phone):
            raise serializers.ValidationError(
                "Phone number must be 10 digits long and contain only numbers."
            )

        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username', None)
        if not username:
            validated_data['username'] = validated_data['email']

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

   

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    