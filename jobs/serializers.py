from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model= Job
        fields= '__all__'
        read_only_fields= ('recruiter', 'created_at', 'updated_at')
        
class FilteredJobSerializer(serializers.ModelSerializer):
    class Meta:
        model= Job
        fields= [
            'id', 'title', 'description', 'location',
            'skills_required', 'salary_range', 'min_experience',
            'created_at'
        ]