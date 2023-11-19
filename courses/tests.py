from django.core.paginator import Paginator
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@course.com',
                                        role='moderator',
                                        phone='123123123',
                                        city='city')
        self.user.set_password('test')
        self.user.save()

        self.course = Course.objects.create(title='test course',
                                            description='test description',
                                            user=self.user)

        self.lesson = Lesson.objects.create(title='test lesson',
                                            course=self.course,
                                            description='test description',
                                            video_url='https://www.youtube.com/',
                                            user=self.user)

        response = self.client.post(reverse('users:token_obtain_pair'),
                                    data={'email': self.user.email, 'password': 'test'})

        self.access_token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_retrieve_lesson(self):
        response = self.client.get(
            reverse('courses:get_lesson', kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': self.lesson.title,
                'course': self.lesson.course.title,
                'description': self.lesson.description,
                'user': self.lesson.user_id,
                'video_url': self.lesson.video_url
            }
        )

    def test_list_lesson(self):
        response = self.client.get(
            reverse('courses:list_lesson')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{
                'id': self.lesson.id,
                'title': self.lesson.title,
                'course': self.lesson.course.title,
                'description': self.lesson.description,
                'user': self.lesson.user_id,
                'video_url': self.lesson.video_url
            }]
        )

    def test_update_lesson(self):
        data = {
            'title': 'test_lesson_1',
            'course': 'test course',
            'description': 'test description',
            'video_url': 'https://www.youtube.com/1'
        }

        response = self.client.put(
            reverse('courses:update_lesson', kwargs={'pk': self.lesson.id}), data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'test_lesson_1',
                'course': self.lesson.course.title,
                'description': 'test description',
                'user': self.lesson.user_id,
                'video_url': 'https://www.youtube.com/1'
            }
        )

    def test_create_lesson(self):
        data = {
            'title': 'test_lesson_2',
            'course': 'test course',
            'description': 'test description',
            'video_url': 'https://www.youtube.com/2'
        }

        response = self.client.post(
            reverse('courses:create_lesson'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_delete_lesson(self):
        response = self.client.delete(
            reverse('courses:delete_lesson', kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(Lesson.objects.all().count(), 0)

    def tearDown(self):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()


class SubscriptionTestCase(LessonTestCase):

    def test_subscribe_course(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
        }

        response = self.client.post(reverse('courses:subscribe'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).exists(), True)

        response = self.client.delete(reverse('courses:unsubscribe', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).exists(), False)
