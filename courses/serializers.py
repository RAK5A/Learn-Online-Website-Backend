from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Course, Lesson

User = get_user_model()


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order']


class CourseListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    lesson_count = serializers.IntegerField(source='lessons.count', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher_name', 'lesson_count']

    def get_teacher_name(self, obj):
        return obj.teacher.username if obj.teacher else None


class CourseDetailSerializer(CourseListSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ['lessons']


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(source='first_name', max_length=150)
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
        )
        student_group, _ = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)
        return user