import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from web.forms import AuthenticationForm, RegistrationForm
from web.models import Institute, Speciality, StudyPlan, User, StudyPlanDiscipline
from web.tools.load_data_tools import (
    deactivate,
    load_disciplines,
    load_faculties,
    load_specialities,
    load_study_plans,
)
from web.tools.parsing_tools import parse_html_table
from web.tools.serializing_tools import disciplines_to_json
from web.tools.web_tools import (
    begin_connection,
    end_connection,
    get_courses,
    get_faculties,
    get_html_table,
    get_specialities,
    get_study_plans,
    push_button,
    set_course,
    set_faculty,
    set_speciality,
    set_study_plan,
)


@login_required
def main_view(request):
    context = {
        "institutes": Institute.objects.filter(is_active=True),
        "specialities": Speciality.objects.filter(is_active=True),
        "study_plans": StudyPlan.objects.filter(is_active=True),
        "failure": False,
        "data": [],
    }
    if request.method == "POST":
        post_data = request.POST
        study_plan = StudyPlan.objects.filter(name=post_data["study_plan"], is_active=True)
        if not study_plan.exists():
            context["failure"] = True
            return render(request, "main.html", context)

        study_plan = study_plan.first()
        disciplines = StudyPlanDiscipline.objects.filter(study_plan=study_plan, is_active=True)
        if not disciplines.exists():
            context["failure"] = True
            return render(request, "main.html", context)

        context["data"] = disciplines_to_json(disciplines)

    return render(request, "main.html", context=context)


def registration_view(request):
    is_success = False
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = User(
                username=form.cleaned_data["username"], email=form.cleaned_data["email"]
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            login(request, user)
            return redirect("main")
    return render(
        request, "registration.html", {"form": form, "is_success": is_success}
    )


def auth_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "auth.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
def update_data_view(request):
    if not request.user.is_superuser:
        return redirect("main")
    try:
        driver = begin_connection()
        faculties = get_faculties(driver)
        deactivate()
        load_faculties(faculties)
    except Exception as error:
        logging.error(error)
        return redirect("main")

    for institute in Institute.objects.all().order_by("id"):
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

        for speciality in Speciality.objects.filter(institute=institute).order_by("id"):
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

            for study_plan in StudyPlan.objects.filter(speciality=speciality).order_by("id"):
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
    return redirect("main")
