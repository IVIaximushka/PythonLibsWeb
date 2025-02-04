from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Institute(models.Model):
    name = models.CharField(max_length=100)
    school = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Speciality(models.Model):
    name = models.CharField(max_length=200)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class StudyPlan(models.Model):
    name = models.CharField(max_length=200)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Discipline(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=100)


class StudyPlanDiscipline(models.Model):
    is_active = models.BooleanField(default=True)
    course = models.SmallIntegerField()
    semester = models.SmallIntegerField()
    exam = models.BooleanField()
    test = models.BooleanField()
    lecture = models.IntegerField()
    practice = models.IntegerField()
    lab = models.IntegerField()
    by_choice = models.BooleanField(default=False)
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
