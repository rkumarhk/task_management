from .models import Project, Task, Comment
from rest_framework import serializers
from users.serializers import UserSerializer
import re

class ProjectCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Project
        fields = ['id', 'name', 'status', 'description']



class ProjectListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Project
        fields = ['id', 'name', 'status', 'description']



class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 
            'title',
            'description',
            'project',
            'assigned_to',
            'status',
            'priority',
            'due_date',
            'estimated_hours',
        ]

    def validate_estimated_hours(self, value):
        if value and value <= 0:
            raise serializers.ValidationError("Estimated hours must be greater than 0")
        return value

class TaskListSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(many=True, read_only=True)
    project = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'project',
            'assigned_to',
            'status',
            'created_by',
            'priority',
            'due_date',
            'estimated_hours',
            'actual_hours',
            'created_at',
            'updated_at',
            'is_active'
        ]

    def get_project(self, obj):
        return {
            'id': obj.project.id,
            'name': obj.project.name
        }

   
class CommentCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'author',
            'content',
            'attachment',
            'parent_comment',
            'replies',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.parent_comment is None:
            replies = obj.replies.filter(is_active=True)
            return CommentCreateSerializer(replies, many=True).data
        return []