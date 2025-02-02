from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from web.models import Institute, Speciality, StudyPlan


def begin_connection() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://shelly.kpfu.ru/e-ksu/study_plan_for_web")
    return driver


def end_connection(driver: webdriver.Chrome) -> None:
    driver.quit()


def get_faculties(driver: webdriver.Chrome) -> dict:
    faculty_element = Select(driver.find_element(By.NAME, "p_faculty"))
    faculty_list = list(map(lambda x: x.text, faculty_element.options))
    faculties = {}
    institute, school = "", ""
    for faculty in faculty_list:
        if "Институт вычислительной математики" in faculty:
            if " " * 12 in faculty:
                school = faculty.strip()
                faculties[institute].append(school)
            elif " " * 8 in faculty:
                institute = faculty.strip()
                faculties[institute] = []
    return faculties


def set_faculty(driver: webdriver.Chrome, faculty: Institute) -> None:
    faculty_element = Select(driver.find_element(By.NAME, "p_faculty"))
    faculty_element.select_by_visible_text(" " * (12 if faculty.school else 8) + faculty.name)


def get_specialities(driver: webdriver.Chrome) -> list[str]:
    speciality_element = Select(driver.find_element(By.NAME, "p_speciality"))
    speciality_list = list(
        filter(lambda x: x, map(lambda x: x.text, speciality_element.options))
    )
    return speciality_list


def set_speciality(driver: webdriver.Chrome, speciality: Speciality) -> None:
    speciality_element = Select(driver.find_element(By.NAME, "p_speciality"))
    speciality_element.select_by_visible_text(speciality.name)


def get_study_plans(driver: webdriver.Chrome) -> list[str]:
    study_plan_element = Select(driver.find_element(By.NAME, "p_sp"))
    study_plan_list = list(
        filter(lambda x: x, map(lambda x: x.text, study_plan_element.options))
    )
    return study_plan_list


def set_study_plan(driver: webdriver.Chrome, study_plan: StudyPlan) -> None:
    study_plan_element = Select(driver.find_element(By.NAME, "p_sp"))
    study_plan_element.select_by_visible_text(study_plan.name)


def get_courses(driver: webdriver.Chrome) -> list[str]:
    course_element = Select(driver.find_element(By.NAME, "p_course"))
    course_list = list(
        filter(lambda x: x.isdigit(), map(lambda x: x.text, course_element.options))
    )
    return course_list


def set_course(driver: webdriver.Chrome, course: str) -> None:
    course_element = Select(driver.find_element(By.NAME, "p_course"))
    course_element.select_by_visible_text(course)


def push_button(driver: webdriver.Chrome) -> None:
    button = driver.find_element(By.XPATH, "//input[@value='Выбрать']")
    button.click()


def get_html_table(driver: webdriver.Chrome) -> str:
    html_table = driver.find_element(By.CLASS_NAME, "T_TABLE")
    return html_table.get_attribute("innerHTML")
