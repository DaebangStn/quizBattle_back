from django.db import models
from django.contrib.auth.models import User
import random


class Room(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(max_length=50, blank=False, unique=True)
    host = models.ForeignKey(User, related_name='room_host', null=False, blank=False, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='room_participants')
    type = models.PositiveSmallIntegerField(default=0)
    round = models.PositiveSmallIntegerField(default=0)
    quiz = models.CharField(max_length=150, blank=True, null=True)
    choices = models.TextField()
    answer = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'Room: {}'.format(self.name)

    def check_if_host(self, user):
        return self.host == user

    def check_if_participants(self, user):
        return user in self.participants.all()

    def submit_answer(self, answer):
        if self.answer == answer:
            self.round += 1
            if self.type == 0:  # 00 X 00
                num1 = random.randrange(10, 100)
                num2 = random.randrange(10, 100)
                ans = num1 * num2
                quiz = '{} x {}'.format(num1, num2)

                self.answer = ans
                self.quiz = quiz

            elif self.type == 1:  # 00 X 00 + 00
                num1 = random.randrange(10, 100)
                num2 = random.randrange(10, 100)
                num3 = random.randrange(10, 100)
                ans = num1 * num2 + num3
                quiz = '{} x {} + {}'.format(num1, num2, num3)

                self.answer = ans
                self.quiz = quiz

            self.save()
            return True
        else:
            return False
