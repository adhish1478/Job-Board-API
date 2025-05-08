from rest_framework import serializers
from .models import Profile, JobSeekerProfile, RecruiterProfile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        exclude= ['user']

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    # Including fields from Profile model
    full_name = serializers.CharField(source='profile.full_name')
    bio = serializers.CharField(source='profile.bio')
    phone = serializers.CharField(source='profile.phone')
    class Meta:
        model= JobSeekerProfile
        fields=['full_name', 'bio', 'phone', 'resume', 'skills']  # This will include all fields in the JobSeekerProfile model

class RecruiterProfileSerializer(serializers.ModelSerializer):
    # Including fields from Profile model
    full_name = serializers.CharField(source='profile.full_name')
    bio = serializers.CharField(source='profile.bio')
    phone = serializers.CharField(source='profile.phone')
    class Meta:
        model= RecruiterProfile
        fields= ['full_name', 'bio', 'phone', 'company_name', 'designation']  # This will include all fields in the RecruiterProfile model
        

