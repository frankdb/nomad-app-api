from rest_framework import serializers

from api.models import Employer, Job


class JobSerializer(serializers.ModelSerializer):
    employer = serializers.PrimaryKeyRelatedField(
        queryset=Employer.objects.all(), required=False
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "requirements",
            "salary",
            "location",
            "employer",
            "posted_date",
        ]
        read_only_fields = ["posted_date"]

    def create(self, validated_data):
        validated_data["employer"] = self.context["request"].user.employer
        return super().create(validated_data)
