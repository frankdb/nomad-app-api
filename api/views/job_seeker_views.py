from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.job_board import Application
from api.serializers.application_serializers import JobSeekerApplicationSerializer
from api.serializers.job_seeker_serializers import JobSeekerUpdateSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class JobSeekerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        if not hasattr(request.user, "jobseeker"):
            return Response(
                {"error": "Only job seekers can update this information"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = JobSeekerUpdateSerializer(
            request.user.jobseeker, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerApplicationListView(generics.ListAPIView):
    serializer_class = JobSeekerApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        if not hasattr(self.request.user, "jobseeker"):
            return Application.objects.none()

        return (
            Application.objects.select_related("job", "job__employer")
            .filter(applicant=self.request.user.jobseeker)
            .order_by("-applied_date")
        )
