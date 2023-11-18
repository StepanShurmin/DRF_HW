from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название курса')
    preview = models.ImageField(upload_to='courses/', verbose_name='Картинка', **NULLABLE)
    description = models.TextField(verbose_name='Описание курса')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    description = models.TextField(verbose_name='Описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='картинка', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
