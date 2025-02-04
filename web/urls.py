from django.urls import path

from web.views import main_view, update_data_view, registration_view, auth_view, logout_view

urlpatterns = [
    path("", main_view, name="main"),
    path("update/", update_data_view, name="update"),
    path('registration/', registration_view, name='registration'),
    path('authentication/', auth_view, name='authentication'),
    path('logout/', logout_view, name='logout'),
]
