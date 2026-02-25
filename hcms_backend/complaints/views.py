from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .utils import calculate_priority, calculate_sla_deadline
from .models import Complaint
from .serializers import ComplaintSerializer
from rest_framework.parsers import MultiPartParser, FormParser



# ===============================
# STUDENT: RAISE COMPLAINT
# ===============================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def raise_complaint(request):
    data = request.data

    required_fields = [
        'student_name',
        'room_number',
        'hostel_name',
        'phone_number',
        'title',
        'description'
    ]

    for field in required_fields:
        if not data.get(field):
            return Response(
                {"error": f"{field} is required"},
                status=400
            )

    priority = calculate_priority(data['title'], data['description'])
    sla_deadline = calculate_sla_deadline(priority)

    complaint = Complaint.objects.create(
        student=request.user,
        student_name=request.data.get('student_name'),
        room_number=request.data.get('room_number'),
        hostel_name=request.data.get('hostel_name'),
        phone_number=request.data.get('phone_number'),
        title=request.data.get('title'),
        description=request.data.get('description'),
        image=request.FILES.get('image'),
        priority=priority,
        sla_deadline=sla_deadline
    )

    # ✅ EMAIL SAFE TRIGGER
    if request.user.email:
        send_mail(
            subject="Complaint Registered Successfully",
            message=f"""
Hello {complaint.student_name},

Your complaint has been registered successfully.

Title: {complaint.title}
Hostel: {complaint.hostel_name}
Room: {complaint.room_number}

Regards,
HCMS Team
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=True
        )

    return Response(
        {"message": "Complaint submitted successfully"},
        status=201
    )



# ===============================
# USER / STAFF / ADMIN: LIST COMPLAINTS
# ===============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_complaints(request):
    if request.user.is_staff or request.user.is_superuser:
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(student=request.user)

    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)


# ===============================
# STAFF / ADMIN: UPDATE STATUS
# ===============================
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_complaint_status(request, id):
    if not (request.user.is_staff or request.user.is_superuser):
        return Response({"error": "Unauthorized"}, status=403)

    try:
        complaint = Complaint.objects.get(id=id)
    except Complaint.DoesNotExist:
        return Response({"error": "Complaint not found"}, status=404)

    status_value = request.data.get("status")
    if not status_value:
        return Response({"error": "Status required"}, status=400)

    complaint.status = status_value
    complaint.save()

    send_mail(
        subject="Complaint Status Updated",
        message=f"""
Hello {complaint.student.username},

Your complaint "{complaint.title}" status is now:
{complaint.status}

Regards,
HCMS Team
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[complaint.student.email],
        fail_silently=True
    )

    return Response({"message": "Status updated"})


# ===============================
# ADMIN: ASSIGN COMPLAINT
# ===============================
@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_complaint(request, id):
    try:
        complaint = Complaint.objects.get(id=id)
    except Complaint.DoesNotExist:
        return Response({"error": "Complaint not found"}, status=404)

    staff_id = request.data.get("staff_id")
    if not staff_id:
        return Response({"error": "Staff ID required"}, status=400)

    try:
        staff = User.objects.get(id=staff_id, is_staff=True)
    except User.DoesNotExist:
        return Response({"error": "Invalid staff user"}, status=400)

    complaint.assigned_staff = staff
    complaint.status = "In Progress"
    complaint.save()

    return Response({"message": "Complaint assigned"})


# ===============================
# STAFF: VIEW ASSIGNED COMPLAINTS
# ===============================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_complaints(request):
    if not request.user.is_staff:
        return Response({"error": "Unauthorized"}, status=403)

    complaints = Complaint.objects.filter(assigned_staff=request.user)
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)


# ===============================
# ADMIN: LIST STAFF
# ===============================
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_staff(request):
    staff = User.objects.filter(is_staff=True, is_superuser=False)
    return Response([{"id": s.id, "username": s.username} for s in staff])


# ===============================
# ADMIN: ALL COMPLAINTS (DASHBOARD)
# ===============================
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_all_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)
