from django.conf.urls import url
import django.contrib.auth.views
from project.views import *
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    url(
        r'^$',
        Login.as_view(),
        name='login'),

    url(
        r'^first_session/(?P<activation_key>\w+)$',
        First_Session.as_view(),
        name='first_session'),

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
        r'^update-users/(?P<id>\w+)$',
        Update_Users.as_view(),
        name='update_users'),

    url(
        r'^delete-user/(?P<id>\w+)$',
        DeleteUser,
        name='delete_user'),

    url(r'^reset/password_reset$',
        password_reset,
        {'template_name': 'registration/page-forgot-password.html',
        'email_template_name': 'registration/password-reset_email.html'},
        name="password_reset"),

    url(r'^reset/password_reset_done$',
        password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        name="password_reset_done"),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'temaplate_name':'registration/page-change-password.html' },
        name = "password_reset_confirm"),

    url(r'^reset\done$',
        password_reset_complete,
        {'template_name':'registration/password_reset-complete.html'},
        name="password_reset_complete"),

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

