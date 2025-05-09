from django.urls import path
from .views import JobListCreateView, JobDetailView

urlpatterns=[
    path('recruiter/jobs/', JobListCreateView.as_view(), name='recruiter-jobs'),
    path('recruiter/jobs/<int:pk>/', JobDetailView.as_view(), name='recruiter-job-detail'),
]