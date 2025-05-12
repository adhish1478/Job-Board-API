from django.urls import path
from .views import MyApplicationsView, ApplyToJobView, ApplicationToViewJob

urlpatterns= [
    path('apply/<int:job_id>/', ApplyToJobView.as_view(), name= 'apply_to_job'),
    path('my-applications/', MyApplicationsView.as_view(), name= 'my_applications'),
    path('recruiter/jobs/<int:job_id>/applicants/', ApplicationToViewJob.as_view(), name= 'application_to_view_job')
]