from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny


# Create your views here.
class RegisterView(APIView):
    permission_classes= [AllowAny] # Open Endpoints

    def post(self, request):
        data= request.data
        if User.objects.filter(username= data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email= data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user= User.objects.create(
            username= data['username'],
            email= data['email'],
            password= make_password(data['password'])
        )
