from django.contrib import admin
from . models import Project, Task, Comment

admin.site.register(Project)
admin.site.register(Task)   
admin.site.register(Comment)
# Register your models here.
