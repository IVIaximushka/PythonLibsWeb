from django.contrib import admin

from web.models import Institute, Speciality, StudyPlan, Discipline


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


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(StudyPlan, StudyPlanAdmin)
admin.site.register(Discipline, DisciplineAdmin)
