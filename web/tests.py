import pytest
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magistrant.settings')
django.setup()
from .models import Institute, Speciality, StudyPlan, Discipline, StudyPlanDiscipline
from web.tools.load_data_tools import deactivate, load_faculties, load_specialities, load_study_plans


@pytest.mark.django_db
def test_institute_creation():
    institute = Institute.objects.create(name='Тестовый институт', school=True)
    assert institute.name == 'Тестовый институт'
    assert institute.school is True
    assert institute.is_active is True


@pytest.mark.django_db
def test_speciality_creation():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    assert speciality.name == 'Тестовая специальность'
    assert speciality.institute == institute
    assert speciality.is_active is True


@pytest.mark.django_db
def test_study_plan_creation():
    institute = Institute.objects.create(name='Тестовый институт')
    speciality = Speciality.objects.create(name='Тестовая специальность', institute=institute)
    study_plan = StudyPlan.objects.create(name='Тестовый учебный план', speciality=speciality)
    assert study_plan.name == 'Тестовый учебный план'
    assert study_plan.speciality == speciality
    assert study_plan.is_active is True


@pytest.mark.django_db
def test_discipline_creation():
    discipline = Discipline.objects.create(name='Тестовая дисциплина')
    assert discipline.name == 'Тестовая дисциплина'
    assert discipline.is_active is True


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
    assert study_plan_discipline.exam is True
    assert study_plan_discipline.test is False
    assert study_plan_discipline.lecture == 10
    assert study_plan_discipline.practice == 5
    assert study_plan_discipline.lab == 2
    assert study_plan_discipline.by_choice is False


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


@pytest.mark.django_db
def test_deactivate():
    Institute.objects.create(name='Test Institute', id='1', is_active=True)
    Speciality.objects.create(name='Test Speciality', id='1', institute_id='1', is_active=True)
    StudyPlan.objects.create(name='Test Study Plan', speciality_id='1', is_active=True)
    Discipline.objects.create(name='Test Discipline', is_active=True)

    deactivate()

    assert Institute.objects.first().is_active is False
    assert Speciality.objects.first().is_active is False
    assert StudyPlan.objects.first().is_active is False
    assert Discipline.objects.first().is_active is False


@pytest.mark.django_db
def test_load_faculties():
    faculties = {
        'Institute A': ['School A1', 'School A2'],
        'Institute B': []
    }

    load_faculties(faculties)

    assert Institute.objects.count() == 3
    assert Institute.objects.filter(name='School A1', school=True).exists()
    assert Institute.objects.filter(name='School A2', school=True).exists()
    assert Institute.objects.filter(name='Institute B', school=False, is_active=True).exists()


@pytest.mark.django_db
def test_load_specialities():
    institute = Institute.objects.create(name='Test Institute')
    specialities = ['Speciality A', 'Speciality B']

    load_specialities(institute, specialities)

    assert Speciality.objects.count() == 2
    assert Speciality.objects.filter(name='Speciality A', institute=institute).exists()
    assert Speciality.objects.filter(name='Speciality B', institute=institute).exists()


@pytest.mark.django_db
def test_load_study_plans():
    institute = Institute.objects.create(name='Test Institute')
    speciality = Speciality.objects.create(name='Test Speciality', institute=institute)
    study_plans = ['Plan A', 'Plan B']

    load_study_plans(speciality, study_plans)

    assert StudyPlan.objects.count() == 2
    assert StudyPlan.objects.filter(name='Plan A', speciality=speciality).exists()
    assert StudyPlan.objects.filter(name='Plan B', speciality=speciality).exists()
