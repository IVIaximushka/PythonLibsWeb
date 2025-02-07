from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Institute(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название института")
    school = models.BooleanField(default=False, verbose_name="Является подразделением института")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "институт"
        verbose_name_plural = "институты"


class Speciality(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название специальности")
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, verbose_name="Институт")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "специальность"
        verbose_name_plural = "специальности"


class StudyPlan(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название учебного плана")
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, verbose_name="Специальность")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "учебный план"
        verbose_name_plural = "учебные планы"


class Discipline(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название дисциплины")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "дисциплина"
        verbose_name_plural = "дисциплины"


class StudyPlanDiscipline(models.Model):
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    course = models.SmallIntegerField(verbose_name="Курс")
    code = models.CharField(max_length=100, verbose_name="Код")
    semester = models.SmallIntegerField(verbose_name="Семестр")
    exam = models.BooleanField(verbose_name="Экзамен")
    test = models.BooleanField(verbose_name="Зачёт")
    lecture = models.IntegerField(verbose_name="Лекции")
    practice = models.IntegerField(verbose_name="Практика")
    lab = models.IntegerField(verbose_name="Лабораторные")
    by_choice = models.BooleanField(default=False, verbose_name="По выбору")
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, verbose_name="Учебный план")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="Дисциплина")

    class Meta:
        verbose_name = "учебный план - дисциплина"
        verbose_name_plural = "учебный план - дисциплина"
