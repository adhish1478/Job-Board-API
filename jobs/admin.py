from django.contrib import admin
from .models import Job

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'location', 'skills_required')
    list_filter = ('is_active', 'location', 'created_at')