from django.conf.urls import url
import django.contrib.auth.views
from project.views import *
from role.views import *

urlpatterns = [

    url(
        r'^role/',
        Role.as_view(),
        name='role'),

    url(
        r'^add-role',
        AddRole.as_view(),
        name='add_role'),

    url(
        r'^delete-role/(?P<id>\w+)$',
        DeleteRole,
        name='delete_role'),

    url(
        r'^update-role/(?P<id>\w+)$',
        UpdateRole.as_view(),
        name='update_role'),

    url(
        r'^ajax/role/$',
        ViewRole,
        name='view_role'),

]

