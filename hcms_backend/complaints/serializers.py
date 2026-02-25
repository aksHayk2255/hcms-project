from rest_framework import serializers
from .models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    # 👇 EXTRA FIELDS FROM USER MODEL
    student_username = serializers.CharField(
        source="student.username", read_only=True
    )
    student_email = serializers.EmailField(
        source="student.email", read_only=True
    )
    sla_deadline = serializers.DateTimeField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_at",
            "sla_deadline",
            "is_overdue",
            "priority",

            # 👇 student-linked details
            "student_username",
            "student_email",

            # 👇 complaint form details
            "student_name",
            "room_number",
            "hostel_name",
            "phone_number",

            # 👇 staff assignment
            "assigned_staff",
            # uploaded image
            "image",
        ]
