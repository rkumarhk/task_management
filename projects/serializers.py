from .models import Project
from rest_framework import serializers
import re

class ProjectCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Project
        fields = ['id', 'name', 'status', 'description']



class ProjectListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Project
        fields = ['id', 'name', 'status', 'description']



   