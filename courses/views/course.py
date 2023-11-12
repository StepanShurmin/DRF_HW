from rest_framework import viewsets

from courses.models import Course
from courses.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()