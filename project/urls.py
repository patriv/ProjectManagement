from django.conf.urls import url
import django.contrib.auth.views
from project.views import *

urlpatterns = [
    url(
        r'^$',
        Login.as_view(),
        name='login'),
    url(
        r'^project',
        Home.as_view(),
        name='project'),
    url(
    r'^users',
    Users.as_view(),
    name='users'),

    url(
    r'^new-users',
    New_Users.as_view(),
    name='new_users'),

    url(
    r'^update-users',
    Update_Users.as_view(),
    name='update_users'),

    url(
    r'^forgot-password',
    Forgot_Password.as_view(),
    name='forgot_password'),

    url(
    r'^change-password',
    Change_Password.as_view(),
    name='change_password'),

    url(
        r'^new-project',
        New_Project.as_view(),
        name='new_project'),

    url(
        r'^profile',
        Profile.as_view(),
        name='profile'),

    url(
        r'^update-project',
        Update_Project.as_view(),
        name='update_project'),

    url(
        r'^detail-project',
        Detail_Project.as_view(),
        name='detail_project'),

    url(
    r'^logout',
    django.contrib.auth.views.logout,
    {
        'next_page': 'login'
    },
    name='logout'),
]

