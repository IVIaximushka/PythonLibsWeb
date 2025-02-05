import pandas as pd

from web.models import Discipline, Institute, Speciality, StudyPlan, StudyPlanDiscipline


def deactivate():
    Institute.objects.all().update(is_active=False)
    Speciality.objects.all().update(is_active=False)
    StudyPlan.objects.all().update(is_active=False)
    Discipline.objects.all().update(is_active=False)


def load_faculties(faculties: dict) -> None:
    for institute in faculties:
        if faculties[institute]:
            for school in faculties[institute]:
                inst, created = Institute.objects.get_or_create(name=school, school=True)
        else:
            inst, created = Institute.objects.get_or_create(name=institute)
        if not created:
            inst.is_active = True
            inst.save()


def load_specialities(institute: Institute, specialities: list[str]) -> None:
    for speciality in specialities:
        spec, created = Speciality.objects.get_or_create(name=speciality, institute=institute)
        if not created:
            spec.is_active = True
            spec.save()


def load_study_plans(speciality: Speciality, study_plans: list[str]) -> None:
    for study_plan in study_plans:
        st_plan, created = StudyPlan.objects.get_or_create(name=study_plan, speciality=speciality)
        if not created:
            st_plan.is_active = True
            st_plan.save()


def _save_discipline(study_plan: StudyPlan, discipline: pd.Series, course: int, semester, by_choice) -> None:
    string_semester = "first" if semester == 1 else "second"
    disc, created = Discipline.objects.get_or_create(name=discipline["name"])
    if not created:
        disc.is_active = True
        disc.save()

    st_plan_disc, created = StudyPlanDiscipline.objects.get_or_create(
        course=course,
        semester=semester,
        code=discipline["id"],
        exam=(discipline[f"{string_semester}_ex"] == "+"),
        test=(discipline[f"{string_semester}_test"] == "+"),
        lecture=int(discipline[f"{string_semester}_lec"]),
        practice=int(discipline[f"{string_semester}_prac"]),
        lab=int(discipline[f"{string_semester}_lab"]),
        study_plan=study_plan,
        discipline=disc,
        by_choice=by_choice
    )
    if not created:
        st_plan_disc.is_active = True
        st_plan_disc.save()


def _save_discipline_by_semester(study_plan: StudyPlan, discipline: pd.Series, course: int, by_choice=False) -> None:
    if isinstance(discipline["first_lec"], str):
        _save_discipline(study_plan, discipline, course, 1, by_choice=by_choice)
    if isinstance(discipline["second_lec"], str):
        _save_discipline(study_plan, discipline, course, 2, by_choice=by_choice)


def load_disciplines(study_plan: StudyPlan, data: pd.DataFrame, course: int) -> None:
    disciplines = data.copy()
    disciplines = disciplines[disciplines["id"].notna()]
    by_choice = data[data["name"].str.contains("по выбору ", case=False)]
    for _, discipline in by_choice.iterrows():
        _save_discipline_by_semester(study_plan, discipline, course, by_choice=True)
        disciplines_by_choice = data[
            data["id"].notna()
            & data["id"].str.contains(discipline["id"])
            & (data["id"] != discipline["id"])
        ]

        for _, discipline_by_choice in disciplines_by_choice.iterrows():
            _save_discipline_by_semester(study_plan, discipline_by_choice, course, by_choice=True)

        disciplines = disciplines[~(disciplines["id"].str.contains(discipline["id"]))]

    for _, discipline in disciplines.iterrows():
        _save_discipline_by_semester(study_plan, discipline, course)
