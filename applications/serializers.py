from rest_framework import serializers
from .models import JobApplication
from accounts.models import Profile

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model= JobApplication
        fields=['id', 'job', 'cover_letter', 'resume', 'applied_at', 'status']
        read_only_fields= ['job', 'applicant', 'applied_at', 'status']


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    applicant= serializers.SerializerMethodField()
    resume= serializers.SerializerMethodField()
    class Meta:
        model= JobApplication
        fields= ['id', 'job', 'applicant', 'cover_letter', 'resume', 'applied_at', 'status']
        read_only_fields= ['job', 'applicant', 'applied_at', 'status']

    def get_applicant(self, obj):
        profile= obj.applicant
        return {
            'full_name': profile.full_name,
            'phone': profile.phone,
            'bio': profile.bio
        }

    def get_resume(self, obj):
        if obj.resume:
        # If the user uploaded a resume during application, show it
            return obj.resume.url
        # Else fallback to profile resume
        try:
            return obj.applicant.job_seeker.resume.url
        except:
            return None
        