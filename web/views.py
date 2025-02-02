import logging

from django.shortcuts import render, redirect

from web.models import Institute, Speciality, StudyPlan, Discipline, StudyPlanDiscipline
from web.tools.load_data_tools import deactivate, load_faculties, load_specialities, load_study_plans, \
    load_disciplines
from web.tools.parsing_tools import parse_html_table
from web.tools.web_tools import begin_connection, get_faculties, end_connection, set_faculty, get_specialities, \
    set_study_plan, set_speciality, get_study_plans, get_courses, set_course, push_button, get_html_table


def main_view(request):
    return render(request, 'main.html')


def update_data_view(request):
    try:
        driver = begin_connection()
        faculties = get_faculties(driver)
    except Exception as error:
        logging.error(error)
        return redirect('main')

    deactivate()
    try:
        load_faculties(faculties)
    except Exception as error:
        logging.error(error)
        return redirect('main')

    for institute in Institute.objects.all().order_by('id'):
        try:
            set_faculty(driver, institute)
            specialities = get_specialities(driver)
        except Exception as error:
            logging.error(error)
            continue

        try:
            load_specialities(institute, specialities)
        except Exception as error:
            logging.error(error)

        for speciality in Speciality.objects.filter(institute=institute).order_by('id'):
            try:
                set_speciality(driver, speciality)
                study_plans = get_study_plans(driver)
            except Exception as error:
                logging.error(error)
                continue

            try:
                load_study_plans(speciality, study_plans)
            except Exception as error:
                logging.error(error)

            for study_plan in StudyPlan.objects.filter(speciality=speciality).order_by('id'):
                try:
                    set_study_plan(driver, study_plan)
                    courses = get_courses(driver)
                except Exception as error:
                    logging.error(error)
                    continue

                for course in courses:
                    try:
                        set_course(driver, course)
                        push_button(driver)
                        table = parse_html_table(get_html_table(driver))
                    except Exception as error:
                        logging.error(error)
                        continue

                    try:
                        load_disciplines(study_plan, table, int(course))
                    except Exception as error:
                        logging.error(error)

    end_connection(driver)
    return redirect('main')
