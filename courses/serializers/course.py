from rest_framework import serializers

from courses.models import Course, Lesson
from courses.serializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lessons_set', many=True, read_only=True)

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons',)
