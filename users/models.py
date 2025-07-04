import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.core.serializers.json import DjangoJSONEncoder


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, password=password, name=name, role='Admin')
        user.is_admin = True
        user.save(using=self._db)
        return user
 


class User(AbstractUser):
    
    ROLE_CHOICES = [
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('projectmanager', 'Project Manager'),
        ('projectlead', 'Project Lead'),
        ('developer', 'Developer'),
        ('client', 'Client'),
    ]
    

    ACCOUNT_STATUS = [
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
        ('active', 'Active'),
    ]

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255,blank=True, null=True)
    middle_name = models.CharField(max_length=255,blank=True, null=True)

    country_code = models.CharField(max_length=4,blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    state = models.CharField(max_length=2, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    
    fcm = models.CharField(max_length=255, blank=True, null=True)

    zip_code = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    email = models.EmailField(unique=True)
    job_role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="developer")
    account_status = models.CharField(blank=True, null=True, choices=ACCOUNT_STATUS, max_length=10)

    fcm = models.CharField(max_length=510, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
 
    def __str__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        return True
 
    def has_module_perms(self, app_label):
        return True
 
    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        ordering = 'id',


