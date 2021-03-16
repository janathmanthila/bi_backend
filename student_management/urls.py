from django.urls import path
from .views import *

urlpatterns = [
    path("", get_students, name="Get Students"),
    path("dataset/create/", create_dataset, name="create dataset for analysis"),
    path("dataset/fetch/summery/", fetch_summery_data, name="get data relevant to summery widgets"),
    path("dataset/fetch/chart/", fetch_chart_data, name="get data relevant to chart widgets"),

]

