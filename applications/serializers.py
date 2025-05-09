from rest_framework import serializers
from .models import JobApplication

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobApplication
        fields=['id', 'job', 'cover_letter', 'resume', 'applied_at', 'status']
        read_only_fields= ['applicant', 'applied_at', 'status']