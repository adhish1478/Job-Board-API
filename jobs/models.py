from django.db import models
from accounts.models import Profile
# Create your models here.

class Job(models.Model):
    recruiter= models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posted_jobs')

    title= models.CharField(max_length=100)
    description= models.TextField()
    location= models.CharField(max_length=100)
    skills_required= models.TextField(help_text="Comma separated list of skills")
    salary_range= models.CharField(max_length=50, help_text="e.g. 50000-70000")
    min_experience = models.IntegerField(null=True, blank=True)
    max_experience = models.IntegerField(null=True, blank=True)
    is_active= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.recruiter.full_name}"
    

