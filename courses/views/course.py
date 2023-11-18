from rest_framework import viewsets

from courses.models import Course
from courses.serializers.course import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        permissions_classes = [IsAuthenticated, IsOwner|IsModerator]
        if self.action == 'list':
            permissions_classes = [IsAuthenticated, IsOwner|IsModerator]
        elif self.action == 'create':
            permissions_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permissions_classes == [IsAuthenticated, IsOwner|IsModerator]
        elif self.action == 'update':
            permissions_classes = [IsAuthenticated, IsOwner|IsModerator]
        elif self.action == 'destroy':
            permissions_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permissions_classes]

    def get_queryset(self):
        qst = super().get_queryset()

        if not self.request.user.is_staff:
            qst = qst.filter(user=self.request.user)

        return qst
