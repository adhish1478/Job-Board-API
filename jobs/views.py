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

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
class PublicJobListView(ListAPIView):
    queryset= Job.objects.all()
    serializer_class= JobSerializer
    permission_classes= [AllowAny]
