from django.db import models
from jobs.models import Job
from django.conf import settings
from accounts.models import Profile

class JobApplication(models.Model):
    job= models.ForeignKey(Job, on_delete=models.CASCADE, related_name= 'applications')
    applicant= models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'applications')
    cover_letter= models.TextField(blank= True)
    resume= models.FileField(upload_to= 'applications/resumes/')
    applied_at= models.DateTimeField(auto_now_add= True)
    status= models.CharField(max_length= 20, choices= [
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ], default= 'applied')

    def __str__(self):
        return f'{self.applicant.full_name} - {self.job.title} - {self.status}'
    
