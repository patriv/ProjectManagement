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

    url(
        r'^documents/(?P<pk>\w+)$',
        DocumentsView.as_view(),
        name='documents'),

    url(
        r'^moreUsers/(?P<pk>\w+)$',
        MoreUsersView.as_view(),
        name='more_users'),

    url(
        r'^ajax/table/$',
        ShowTable,
        name='table'),

    url(
        r'^changeStatus/(?P<code>[\w-]+)/(?P<pk>\w+)/$',
        ChangeStatus.as_view(),
        name='change_status'),

    url(
        r'^buttoncloseProject/$',
        ChangeButton,
        name='change_button'),

    url(
        r'^closeProject/(?P<pk>\w+)/$',
        CloseProject,
        name='close_project'),

    url(
        r'^delete-project/(?P<code>\w+)/$',
        DeleteProject,
        name='delete_project'),

]

