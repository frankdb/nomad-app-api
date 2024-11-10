from django.urls import path

from api.views.job_seeker_views import JobSeekerApplicationListView, JobSeekerUpdateView

urlpatterns = [
    path("job-seeker/profile/", JobSeekerUpdateView.as_view(), name="jobseeker-update"),
    path(
        "job-seeker/applications/",
        JobSeekerApplicationListView.as_view(),
        name="jobseeker-applications",
    ),
]
