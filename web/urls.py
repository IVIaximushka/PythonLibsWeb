from django.urls import path

from web.views import main_view, update_data_view

urlpatterns = [
    path('', main_view, name='main'),
    path('update/', update_data_view, name='update'),
]