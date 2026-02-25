from django.urls import path
from .views import (
    raise_complaint,
    list_complaints,
    update_complaint_status,
    assign_complaint,
    staff_complaints,
    admin_all_complaints,
    list_staff,
)

urlpatterns = [
    # Student
    path("raise/", raise_complaint),
    path("list/", list_complaints),

    # Staff
    path("staff/", staff_complaints),
    path("update/<int:id>/", update_complaint_status),

    # Admin
    path("all/", admin_all_complaints),
    path("assign/<int:id>/", assign_complaint),
    path("staff-list/", list_staff),
]
