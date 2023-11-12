from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from courses.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'course', 'description',)
