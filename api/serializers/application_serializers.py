from rest_framework import serializers

from api.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "job",
            "applied_date",
            "status",
            "cover_letter",
        ]
        read_only_fields = ["id", "applied_date", "status", "applicant"]


class JobSeekerApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title")
    company_name = serializers.CharField(source="job.employer.company_name")

    class Meta:
        model = Application
        fields = ["id", "applied_date", "job_title", "company_name", "status"]
