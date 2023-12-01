from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from courses.models import Course
from courses.paginators import CoursesPaginator
from courses.serializers.course import CourseSerializer
from users.permissions import IsOwner, IsModerator
from courses.tasks import send_email_course_update

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursesPaginator

    def get_permissions(self):
        permissions_classes = [IsAuthenticated, IsOwner | IsModerator]
        if self.action == 'list':
            permissions_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'create':
            permissions_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permissions_classes == [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'update':
            permissions_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permissions_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permissions_classes]

    def get_queryset(self):
        qst = super().get_queryset()

        if not self.request.user.is_staff:
            qst = qst.filter(user=self.request.user)

        return qst

    def perform_update(self, serializer):
        new_update = serializer.save()
        if new_update:
            send_email_course_update.delay(course_id=new_update.id)
            new_update.save()
            return Response(serializer.data, status=status.HTTP_200_OK)