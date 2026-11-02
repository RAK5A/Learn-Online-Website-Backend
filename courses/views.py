from rest_framework import generics, permissions

from .models import Course
from .serializers import (
    CourseDetailSerializer,
    CourseListSerializer,
    RegisterSerializer,
)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]