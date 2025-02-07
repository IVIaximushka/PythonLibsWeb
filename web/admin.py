from django.contrib import admin

from web.models import Institute, Speciality, StudyPlan, Discipline, StudyPlanDiscipline


class InstituteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "school", "is_active")
    search_fields = ("id", "name")
    list_filter = ("is_active", "school")


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "institute", "is_active")
    search_fields = ("id", "name", "institute__name")
    list_filter = ("is_active", "institute__name")


class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "speciality", "is_active")
    search_fields = ("id", "name", "speciality__name")
    list_filter = ("is_active", "speciality__institute__name", "speciality__name")


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    search_fields = ("id", "name")
    list_filter = ("is_active",)


class StudyPlanDisciplineAdmin(admin.ModelAdmin):
    list_display = ("id", "study_plan", "discipline", "code", "course", "semester", "exam", "test", "lecture", "practice", "lab", "by_choice")
    search_fields = ("id", "study_plan__name", "discipline__name")
    list_filter = ("is_active", "by_choice", "course", "semester")


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(StudyPlan, StudyPlanAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(StudyPlanDiscipline, StudyPlanDisciplineAdmin)
