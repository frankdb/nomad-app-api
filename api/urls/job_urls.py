from django.urls import path

from api.views.job_views import JobDetailView, JobListCreateView

urlpatterns = [
    path("jobs/", JobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
]
