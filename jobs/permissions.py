from rest_framework.permissions import BasePermission

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        # Allow access only to authenticated users
        return request.user.is_authenticated and request.user.is_recruiter
    
    def has_object_permission(self, request, view, obj):
        # Allow access only to the recruiter who created the job
        return obj.recruiter.user ==  request.user