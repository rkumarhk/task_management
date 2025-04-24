from django.db import models
from users.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    project_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects' )
    team_members = models.ManyToManyField(User, related_name='assigned_projects', blank=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_projects')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='project_owner')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('in_review', 'In Review'),
        ('done', 'Done'),
        ('blocked', 'Blocked')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    project = models.ForeignKey( Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ManyToManyField(User, null=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')

    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField( max_length=10, choices=PRIORITY_CHOICES, default='medium')

    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.DecimalField( max_digits=5, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField( max_digits=5, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class Comment(models.Model):
    task = models.ForeignKey( Task,  on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, related_name='task_comments')
    content = models.TextField()
    attachment = models.FileField( upload_to='task_comments/', null=True, blank=True)
    parent_comment = models.ForeignKey( 'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.email} on {self.task.title}'