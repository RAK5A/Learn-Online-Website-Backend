from django.contrib import admin
from .models import (
    Course, Lesson, Quiz, Question, Choice,
    Enrollment, LessonProgress, Attempt,
)


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'is_published')
    inlines = [LessonInline]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    inlines = [ChoiceInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Attempt)