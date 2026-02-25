from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "student_name",
        "room_number",
        "hostel_name",
        "assigned_staff",
        "status",
        "created_at"
    )
    list_filter = ('status',)
    search_fields = ('title', 'description', 'student__username')
