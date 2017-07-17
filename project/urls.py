from django.conf.urls import url
import django.contrib.auth.views
from project.views import *

urlpatterns = [


    url(
        r'^project',
        Home.as_view(),
        name='project'),

    url(
        r'^new-project',
        New_Project.as_view(),
        name='new_project'),

    url(
        r'^update-project',
        Update_Project.as_view(),
        name='update_project'),

    url(
        r'^detail-project',
        Detail_Project.as_view(),
        name='detail_project'),

    url(
        r'^new-task',
        New_Task.as_view(),
        name='new_task'),

    url(
        r'^ajax/name',
        ValidateName,
        name='validate_name'),


]

