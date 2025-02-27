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
            discipline.exam,
            discipline.test,
        )
    )


def _get_filtered_data(data: list[tuple], semester: int) -> list[tuple]:
    filtered_and_sorted_data = sorted(
        filter(lambda discipline: discipline[2] == semester and discipline[1] != 0, data),
        key=lambda discipline: discipline[1],
    )
    return filtered_and_sorted_data


def _build_diagram():
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    graphic = base64.b64encode(buf.read())
    graphic = graphic.decode("utf-8")
    plt.clf()
    return graphic


def _select_color(discipline: tuple):
    if discipline[3] and discipline[4]:
        return 'purple'
    if discipline[3]:
        return 'red'
    if discipline[4]:
        return 'yellow'
    return 'green'


def _add_diagram(diagram_data: list[tuple], semester: int):
    filtered_and_sorted_data = _get_filtered_data(diagram_data, semester)
    if sum(map(lambda discipline: discipline[1], filtered_and_sorted_data)) != 0:
        plt.figure(figsize=(7, 3))
        plt.barh(
            [i[0] for i in filtered_and_sorted_data],
            [i[1] for i in filtered_and_sorted_data],
            color=[_select_color(i) for i in filtered_and_sorted_data],
        )
        return _build_diagram()
    return None


def _add_pie_diagram(diagram_data: list[tuple], semester: int):
    filtered_and_sorted_data = _get_filtered_data(diagram_data, semester)
    if sum(map(lambda discipline: discipline[1], filtered_and_sorted_data)) != 0:
        plt.figure(figsize=(6, 4))
        plt.pie(
            [i[1] for i in filtered_and_sorted_data],
            labels=[i[0] for i in filtered_and_sorted_data],
            autopct="%1.1f%%"
        )
        return _build_diagram()
    return None


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
                "first_semester_pie": _add_pie_diagram(diagram_data, 1),
                "second_semester_pie": _add_pie_diagram(diagram_data, 2),
            }
        )
        plt.close()
    return data_by_course
