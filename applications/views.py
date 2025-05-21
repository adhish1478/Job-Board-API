from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import JobApplication
from jobs.models import Job
from accounts.models import Profile
from .serializers import JobApplicationSerializer
# Create your views here.

class ApplyToJobView(APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request, job_id):
        user= request.user
        print("AUTHENTICATED USER:", user)
        print("ROLE:", user.role)
        if not hasattr(user, 'role') or user.role != 'job_seeker':
            return Response({'error': 'Only job seekers can apply for jobs'}, status= status.HTTP_403_FORBIDDEN)    
        
        profile= Profile.objects.get(user= user)
        try:
            job= Job.objects.get(id= job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status= status.HTTP_404_NOT_FOUND)
        
        #Check if the user has already applied for the job
        if JobApplication.objects.filter(job= job, applicant= profile).exists():
            return Response({'error': 'You have already applied for this job'}, status= status.HTTP_400_BAD_REQUEST)
        
        # Use uploaded resume if provided, else use the resume from profile
        resume= request.FILES.get('resume') or getattr(getattr(profile, 'job_seeker', None), 'resume', None)

        # If no resume is provided, return an error
        if not resume:
            return Response({'error': 'Resume is required'}, status= status.HTTP_400_BAD_REQUEST)
        
        # Instead of copying request.data, we can directly assign the resume
        data = {
            'job': job.id,  # We set the job ID directly
            'cover_letter': request.data.get('cover_letter', ''),  # If cover letter is provided
            'resume': resume,
        }


        serializer= JobApplicationSerializer(data= data)
        if serializer.is_valid():
            serializer.save(applicant= profile, job= job)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class MyApplicationsView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'job_seeker':
            return Response({'error': 'Only job seekers can view their applications'}, status= status.HTTP_403_FORBIDDEN)
        
        profile= Profile.objects.get(user= request.user)
        applications= JobApplication.objects.filter(applicant= profile).select_related('job')
        serializer= JobApplicationSerializer(applications, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)

#For recruiters to view their applications
from jobs.permissions import IsRecruiter
from .serializers import JobApplicationDetailSerializer
class ApplicationToViewJob(APIView):
    permission_classes= [IsAuthenticated & IsRecruiter]
    def get(self, request, job_id):
        try:
            job= Job.objects.get(id= job_id)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status= status.HTTP_404_NOT_FOUND)
        #check if recruiter has acces to his job
        if job.recruiter.user != request.user:
            return Response({'error': 'You do not have access to this job'}, status= status.HTTP_403_FORBIDDEN)
        applications= JobApplication.objects.filter(job=job).select_related('applicant')
        serializer= JobApplicationDetailSerializer(applications, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)