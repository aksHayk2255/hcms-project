from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email    = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response(
            {"error": "Username, email and password required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,        # ✅ EMAIL SAVED
        password=password
    )

    return Response({
        "message": "User registered successfully",
        "role": "student"
    }, status=201)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    token, _ = Token.objects.get_or_create(user=user)

    role = "student"
    if user.is_superuser:
        role = "admin"
    elif user.is_staff:
        role = "staff"

    return Response({
        "token": token.key,
        "role": role,
        "username": user.username
    })
