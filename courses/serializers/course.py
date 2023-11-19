from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.serializers.lesson import LessonSerializer
from courses.serializers.subscription import SubscriptionSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lessons_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        return Subscription.objects.filter(course=course, user=self.context['request'].user).exists()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'lessons_count', 'lessons', 'is_subscribed',)
