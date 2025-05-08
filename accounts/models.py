from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# Create your models here.
#Custom User manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role='job_seeker', **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email= self.normalize_email(email)
        user= self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password,role= 'admin' ,**extra_fields)
    
#Custom User Model
class CustomUser(AbstractUser, PermissionsMixin):
    username= None
    ROLE_CHOICHES= (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin')
    )
    email= models.EmailField(unique=True)
    role= models.CharField(max_length=20, choices= ROLE_CHOICHES, default='job_seeker')
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects= CustomUserManager()
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email

def upload_to_resume(instance, filename):
    return f'resumes/user_{instance.profile.user.email}/{filename}'
    #<form method="POST" enctype="multipart/form-data"> ---> only to be used in html forms later
    
# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)


    def __str__(self):
        return f"{self.user.email} Profile"

class RecruiterProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='recruiter')
    company_name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.profile.full_name} Recruiter Profile"
    
class JobSeekerProfile(models.Model):
    profile= models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='job_seeker')
    resume= models.FileField(upload_to=upload_to_resume, blank=True)
    skills= models.TextField(blank=True)

    def __str__(self):
        return f"{self.profile.full_name} Job Seeker Profile"