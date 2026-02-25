from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Emergency', 'Emergency'),
]

class Complaint(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_complaints"
    )

    student_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    hostel_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='complaint_images/', null=True, blank=True)  # NEW
    status = models.CharField(max_length=20, default="Pending")
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Low'
    )

    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_complaints"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    sla_deadline = models.DateTimeField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)

    def __str__(self):
        return self.title
