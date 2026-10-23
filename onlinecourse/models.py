
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Exam(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="exams"
    )
    title = models.CharField(max_length=200, default="Mock Exam")

    def __str__(self):
        return self.title


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="questions",
        null=True, blank=True
    )
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        correct_ids = set(
            self.choice_set.filter(is_correct=True).values_list("id", flat=True)
        )
        selected_ids = set(map(int, selected_ids))
        return correct_ids == selected_ids


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice, blank=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
