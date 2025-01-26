from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Institute(models.Model):
    name = models.CharField(max_length=100)


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)


class StudyPlan(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)


class Discipline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    course = models.SmallIntegerField()
    semester = models.SmallIntegerField()
    by_choice = models.BooleanField()
    exam = models.BooleanField()
    test = models.BooleanField()
    lecture = models.IntegerField()
    practice = models.IntegerField()
    lab = models.IntegerField()
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
