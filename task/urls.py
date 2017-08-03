from django.conf.urls import url
import django.contrib.auth.views
from task.views import *

urlpatterns = [
    url(
        r'^new-task/(?P<pk>\w+)$',
        New_Task.as_view(),
        name='new_task'),


    url(
        r'^ajax/gantt/',
        Gantt,
        name='gantt'),

    url(
        r'^update-task/(?P<code>[\w-]+)$',
        Update_Task.as_view(),
        name='update_task'),

]