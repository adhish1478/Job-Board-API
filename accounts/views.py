from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from .models import Profile, RecruiterProfile, JobSeekerProfile
from .utils import get_email_veriification_token
from .tasks import send_verification_mail_async

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
        #  Email verification logic here
        token= get_email_veriification_token(user)
        send_verification_mail_async.delay(user.id, token)
        return Response({
            'message': 'User created successfully, Please check your email to verify your account.',
            'user': {
                'email': user.email,
                'role': user.role
            }
        }, status=status.HTTP_201_CREATED)
# The RegisterView class handles user registration. It checks if the email already exists, creates a new user with the provided email and password, and returns a success message along with the user's email and role.
# The permission_classes attribute is set to AllowAny, which means that this endpoint is open to all users, regardless of authentication status.
        


#GET and PUT for profiles
from .serializers import ProfileSerializer, JobSeekerProfileSerializer, RecruiterProfileSerializer
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes= [IsAuthenticated] # Protected Endpoints

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        if request.user.role == 'recruiter':
            #only for recruiters
            serializer= RecruiterProfileSerializer(profile.recruiter)
        else:
            #only for job seekers
            serializer= JobSeekerProfileSerializer(profile.job_seeker)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        try:
            profile= Profile.objects.get(user= request.user)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        # Check if the user is a recruiter or job seeker and update accordingly
        if request.user.role == 'recruiter':
            #only for recruiters
            serializer= RecruiterProfileSerializer(profile.recruiter, data= request.data, partial= True)
        else:
            #only for job seekers
            serializer= JobSeekerProfileSerializer(profile.job_seeker, data= request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# The UserProfileView class handles user profile retrieval and updating. It uses the IsAuthenticated permission class to ensure that only authenticated users can access this endpoint.


# A view to verify the token
from rest_framework_simplejwt.tokens import AccessToken
class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()
            return Response({'message': 'Email successfully verified.'}, status=200)
        except Exception as e:
            return Response({'error': 'Invalid or expired token.'}, status=400)
        
# View to verify existing user
class ResendVerificationEmailView(APIView):
    permission_classes= [AllowAny]

    def post(self, request):
        email= request.data.get('email')
        try:
            user= User.objects.get(email=email)
            if user.is_verified:
                return Response({'message':'Email already verified'}, status=200)
            token= get_email_veriification_token(user)
            send_verification_mail_async.delay(user.id, token)

            return Response({'message': 'Verification email sent successfully.'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)