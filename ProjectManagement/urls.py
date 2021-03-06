"""ProjectManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from API import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profile-users', views.ProfileUserViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'permission', views.PermissionViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'project-user', views.ProjectUserViewSet)
router.register(r'document', views.DocumentsViewSet)
router.register(r'task', views.TaskViewSet)
router.register(r'task-dependency', views.DependencyViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('project.urls')),
    url(r'^', include('role.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('task.urls')),
    url(r'^API/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]




