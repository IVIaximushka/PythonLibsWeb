from django.db.models import QuerySet

from web.models import StudyPlanDiscipline


def _add_discipline(discipline: StudyPlanDiscipline, data: list):
    data.append(
        {
            "code": discipline.code,
            "name": discipline.discipline.name,
            "course": discipline.course,
            "semester": discipline.semester,
            "exam": discipline.exam,
            "test": discipline.test,
            "lecture": discipline.lecture,
            "practice": discipline.practice,
            "lab": discipline.lab,
        }
    )


def disciplines_to_json(disciplines: QuerySet) -> list[dict]:
    courses = disciplines.order_by("course").values_list("course", flat=True).distinct()
    data_by_course = []
    for course in courses:
        disciplines_by_course = disciplines.filter(course=course)
        data = {"ordinary": [], "by_choice": []}
        by_choice = disciplines_by_course.filter(by_choice=True)
        ordinary = disciplines_by_course.exclude(id__in=by_choice.values("id"))
        if ordinary.exists():
            for discipline in ordinary:
                _add_discipline(discipline, data["ordinary"])

        if by_choice.exists():
            main_by_choice = by_choice.filter(discipline__name__contains="по выбору ")
            for discipline in main_by_choice:
                another_disciplines = by_choice.filter(code__startswith=discipline.code)
                _add_discipline(discipline, data["by_choice"])
                data["by_choice"][-1]["disciplines"] = []

                for another_discipline in another_disciplines:
                    data["by_choice"][-1]["disciplines"].append(another_discipline.discipline.name)
        data_by_course.append({"course": course, "disciplines": data})
    return data_by_course
