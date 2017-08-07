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
        r'^update-project/(?P<pk>\w+)$',
        Update_Project.as_view(),
        name='update_project'),

    url(
        r'^detail-project/(?P<pk>\w+)$',
        Detail_Project.as_view(),
        name='detail_project'),


    url(
        r'^ajax/name/$',
        ValidateName,
        name='validate_name'),

    url(
        r'^ajax/detailProject/$',
        ShowDetails,
        name='show_project'),

    url(
        r'^bar',
        BarProgress,
        name='bar'),

    url(
        r'^ajax/kwargs/$',
        getCode,
        name='kwargs'),

]

