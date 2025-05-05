from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny

User= get_user_model()
# Create your views here.
class RegisterView(APIView):
    permission_classes= [AllowAny] # Open Endpoints

    def post(self, request):
        data= request.data
        if User.objects.filter(email= data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user= User.objects.create(
            email= data['email'],
            password= make_password(data['password']),
            role= data.get('role', 'job_seeker'), # Default role is 'job_seeker'
        )
        return Response({
            'message': 'User created successfully',
            'user': {
                'email': user.email,
                'role': user.role
            }
        }, status=status.HTTP_201_CREATED)
# The RegisterView class handles user registration. It checks if the email already exists, creates a new user with the provided email and password, and returns a success message along with the user's email and role.
# The permission_classes attribute is set to AllowAny, which means that this endpoint is open to all users, regardless of authentication status.

