from django.conf.urls import url
import django.contrib.auth.views
from task.views import *

urlpatterns = [
    url(
        r'^new-task/(?P<pk>\w+)$',
        New_Task.as_view(),
        name='new_task'),
    
]