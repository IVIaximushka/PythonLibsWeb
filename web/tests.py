import pytest
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magistrant.settings')
django.setup()
from .models import Institute, Speciality, StudyPlan, Discipline, StudyPlanDiscipline


@pytest.mark.django_db
def test_institute_creation():
    institute = Institute.objects.create(name='Тестовый институт', school=True)
    assert institute.name == 'Тестовый институт'
    assert institute.school == True
    assert institute.is_active == True


@pytest.mark.django_db
def test_speciality_creation():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    assert speciality.name == 'Тестовая специальность'
    assert speciality.institute == institute
    assert speciality.is_active == True


@pytest.mark.django_db
def test_study_plan_creation():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    study_plan = StudyPlan.objects.create(name='Тестовый учебный план', speciality=speciality)
    assert study_plan.name == 'Тестовый учебный план'
    assert study_plan.speciality == speciality
    assert study_plan.is_active == True


@pytest.mark.django_db
def test_discipline_creation():
    discipline = Discipline.objects.create(name='Тестовая дисциплина')
    assert discipline.name == 'Тестовая дисциплина'
    assert discipline.is_active == True


@pytest.mark.django_db
def test_study_plan_discipline_creation():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    study_plan = StudyPlan.objects.create(name='Тестовый учебный план', speciality=speciality)
    discipline = Discipline.objects.create(name='Тестовая дисциплина')
    study_plan_discipline = StudyPlanDiscipline.objects.create(
        study_plan=study_plan,
        discipline=discipline,
        course=1,
        code='123',
        semester=1,
        exam=True,
        test=False,
        lecture=10,
        practice=5,
        lab=2,
        by_choice=False
    )
    assert study_plan_discipline.study_plan == study_plan
    assert study_plan_discipline.discipline == discipline
    assert study_plan_discipline.course == 1
    assert study_plan_discipline.code == '123'
    assert study_plan_discipline.semester == 1
    assert study_plan_discipline.exam == True
    assert study_plan_discipline.test == False
    assert study_plan_discipline.lecture == 10
    assert study_plan_discipline.practice == 5
    assert study_plan_discipline.lab == 2
    assert study_plan_discipline.by_choice == False


@pytest.mark.django_db
def test_institute_deletion():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    study_plan = StudyPlan.objects.create(name='Тестовый учебный план', speciality=speciality)
    discipline = Discipline.objects.create(name='Тестовая дисциплина')
    study_plan_discipline = StudyPlanDiscipline.objects.create(
        study_plan=study_plan,
        discipline=discipline,
        course=1,
        code='123',
        semester=1,
        exam=True,
        test=False,
        lecture=10,
        practice=5,
        lab=2,
        by_choice=False
    )
    institute.delete()
    assert Institute.objects.count() == 0
    assert Speciality.objects.count() == 0
    assert StudyPlan.objects.count() == 0
    assert StudyPlanDiscipline.objects.count() == 0


@pytest.mark.django_db
def test_speciality_deletion():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    study_plan = StudyPlan.objects.create(name='Тестовый учебный план', speciality=speciality)
    discipline = Discipline.objects.create(name='Тестовая дисциплина')
    study_plan_discipline = StudyPlanDiscipline.objects.create(
        study_plan=study_plan,
        discipline=discipline,
        course=1,
        code='123',
        semester=1,
        exam=True,
        test=False,
        lecture=10,
        practice=5,
        lab=2,
        by_choice=False
    )
    speciality.delete()
    assert Speciality.objects.count() == 0
    assert StudyPlan.objects.count() == 0
    assert StudyPlanDiscipline.objects.count() == 0


@pytest.mark.django_db
def test_study_plan_deletion():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    study_plan = StudyPlan.objects.create(name='Тестовый учебный план', speciality=speciality)
    discipline = Discipline.objects.create(name='Тестовая дисциплина')
    study_plan_discipline = StudyPlanDiscipline.objects.create(
        study_plan=study_plan,
        discipline=discipline,
        course=1,
        code='123',
        semester=1,
        exam=True,
        test=False,
        lecture=10,
        practice=5,
        lab=2,
        by_choice=False
    )
    study_plan.delete()
    assert StudyPlan.objects.count() == 0
    assert StudyPlanDiscipline.objects.count() == 0
