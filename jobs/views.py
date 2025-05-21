from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer
from .permissions import IsRecruiter
from accounts.models import Profile

# Create your views here.
class JobListCreateView(APIView):
    permission_classes= [IsAuthenticated, IsRecruiter]

    def get(self, request):
        jobs= Job.objects.filter(recruiter__user= request.user)
        serializer= JobSerializer(jobs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request):
        profile= Profile.objects.get(user= request.user)
        serializer= JobSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save(recruiter= profile)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class JobDetailView(APIView):
    permission_classes= [IsAuthenticated, IsRecruiter]

    def get_object(self, pk, user):
        try:
            return Job.objects.get(pk=pk, recruiter__user= user)
        except Job.DoesNotExist:
            return None
        
    def put(self, request, pk):
        job= self.get_object(pk, request.user)
        if not job:
            return Response("Job not found", status= status.HTTP_404_NOT_FOUND)
        serializer= JobSerializer(job, data= request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        job= self.get_object(pk, request.user)
        if not job:
            return Response("Job not found", status= status.HTTP_404_NOT_FOUND)
        job.delete()
        return Response("Job deleted successfully", status= status.HTTP_204_NO_CONTENT)



#Filtering jobs and showing them to the public
from .serializers import FilteredJobSerializer
class FilteredJobListView(APIView):
    def get(self, request):
        jobs= Job.objects.all()

        #Optional filtering
        title = request.query_params.get('title')
        location = request.query_params.get('location')
        skills = request.query_params.get('skills')
        min_salary = request.query_params.get('min_salary')
        experience = request.query_params.get('min_experience')

        if title:
            jobs= jobs.filter(title__icontains= title)
        if location:
            jobs= jobs.filter(location__icontains= location)
        if skills:
            jobs= jobs.filter(skills_required__icontains= skills)
        if min_salary:
            jobs= jobs.filter(salary_range__gte= min_salary)
        if experience:
            jobs= jobs.filter(min_experience__lte= experience)

        serializer= FilteredJobSerializer(jobs, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK)