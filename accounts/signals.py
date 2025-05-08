from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile, RecruiterProfile, JobSeekerProfile

@receiver(post_save, sender= CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile= Profile.objects.create(user= instance)

        if instance.role == 'recruiter':
            RecruiterProfile.objects.create(profile= profile)
        elif instance.role == 'job_seeker':
            JobSeekerProfile.objects.create(profile= profile)

@receiver(post_save, sender= CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()