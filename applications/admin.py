from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'applicant', 'applied_at', 'status']
    search_fields = ['job__title', 'applicant__full_name']
    list_filter = ['status', 'applied_at']