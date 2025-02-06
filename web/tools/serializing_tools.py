import base64
import io

from django.db.models import QuerySet
from matplotlib import pyplot as plt, use

from web.models import StudyPlanDiscipline

use("agg")


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


def _add_diagram_data(discipline: StudyPlanDiscipline, data: list) -> None:
    data.append(
        (
            discipline.discipline.name,
            discipline.lecture + discipline.practice + discipline.lab,
            discipline.semester,
        )
    )


def _add_diagram(diagram_data: list[tuple], semester: int):
    filtered_and_sorted_data = sorted(
        filter(lambda discipline: discipline[2] == semester, diagram_data),
        key=lambda discipline: discipline[1],
    )
    plt.barh(
        [i[0] for i in filtered_and_sorted_data],
        [i[1] for i in filtered_and_sorted_data],
    )
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    graphic = base64.b64encode(buf.read())
    graphic = graphic.decode("utf-8")
    plt.clf()
    return graphic


def disciplines_to_json(disciplines: QuerySet) -> list[dict]:
    courses = disciplines.order_by("course").values_list("course", flat=True).distinct()
    data_by_course = []
    for course in courses:
        disciplines_by_course = disciplines.filter(course=course)
        data = {"ordinary": [], "by_choice": []}
        by_choice = disciplines_by_course.filter(by_choice=True)
        ordinary = disciplines_by_course.exclude(id__in=by_choice.values("id"))
        diagram_data = []
        if ordinary.exists():
            for discipline in ordinary:
                _add_discipline(discipline, data["ordinary"])
                _add_diagram_data(discipline, diagram_data)

        if by_choice.exists():
            main_by_choice = by_choice.filter(discipline__name__contains="по выбору ")
            for discipline in main_by_choice:
                another_disciplines = by_choice.filter(code__startswith=discipline.code)
                _add_discipline(discipline, data["by_choice"])
                _add_diagram_data(discipline, diagram_data)
                data["by_choice"][-1]["disciplines"] = []

                for another_discipline in another_disciplines:
                    data["by_choice"][-1]["disciplines"].append(another_discipline.discipline.name)

        data_by_course.append(
            {
                "course": course,
                "disciplines": data,
                "first_semester_diagram": _add_diagram(diagram_data, 1),
                "second_semester_diagram": _add_diagram(diagram_data, 2),
            }
        )
        plt.close()
    return data_by_course
