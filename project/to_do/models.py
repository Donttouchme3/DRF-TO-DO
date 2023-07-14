from django.db import models
from datetime import date

# Create your models here.


class Tasks(models.Model):
    todo = 'to-do'
    in_progress = 'in progress'
    done = 'done'

    STATUS_CHOICES = [
        (todo, 'To-Do'),
        (in_progress, 'In Progress'),
        (done, 'Done'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(default='Дайте описание', verbose_name='Описание')
    start_time = models.DateField(default=date.today, verbose_name='Дата начала')
    end_time = models.DateField(default=date.today, verbose_name='Дата окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


