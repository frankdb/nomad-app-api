from rest_framework import serializers

from api.models import Employer, Job


class JobSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(
        queryset=Employer.objects.all(), required=False
    )
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "requirements",
            "salary",
            "location",
            "employer",
            "posted_date",
        ]
        read_only_fields = ["posted_date", "slug"]

    def create(self, validated_data):
        validated_data["employer"] = self.context["request"].user.employer
        job = Job.objects.create(**validated_data)
        return job
