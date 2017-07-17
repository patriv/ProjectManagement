from django.conf.urls import url
import django.contrib.auth.views
from users.views import *

urlpatterns = [
    url(
        r'^$',
        Login.as_view(),
        name='login'),

    url(
        r'^login',
        user_login,
        name='home'),

    url(
        r'^first_session/(?P<activationKey>\w+)$',
        First_Session.as_view(),
        name='first_session'),

     url(
        r'^users',
        Users.as_view(),
        name='users'),

    url(
        r'^new-users',
        New_Users.as_view(),
        name='new_users'),

    url(
        r'^update-users/(?P<id>\w+)$',
        Update_Users.as_view(),
        name='update_users'),

    url(
        r'^delete-user/(?P<id>\w+)$',
        DeleteUser,
        name='delete_user'),

    url(r'^reset/password_reset$',
        Password_Reset.as_view(),
        name="password_reset"),

    url(r'^reset/(?P<token>.+)$',
        Password_Reset_Confirm.as_view(),
        name='password_reset_confirm'
        ),

    url(
        r'^profile/(?P<id>\w+)$',
        Profile.as_view(),
        name='profile'),

    url(
        r'get_project$',
        get_projects,
        name='get_project'),

    url(
    r'^logout',
    django.contrib.auth.views.logout,
    {
        'next_page': 'login'
    },
    name='logout'),
]

