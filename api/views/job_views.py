from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Job
from api.permissions import IsEmployerOrReadOnly
from api.serializers.job_serializers import JobSerializer


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.select_related("employer").all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsEmployerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)


class JobDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsEmployerOrReadOnly()]

    def get_object(self, pk):
        try:
            return Job.objects.select_related("employer").get(pk=pk)
        except Job.DoesNotExist:
            return None

    def get(self, request, pk):
        job = self.get_object(pk)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobDetailBySlugView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, slug):
        try:
            return Job.objects.select_related("employer").get(slug=slug)
        except Job.DoesNotExist:
            return None

    def get(self, request, slug):
        job = self.get_object(slug)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data)


class EmployerJobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.select_related("employer").filter(
            employer=self.request.user.employer
        )
