from rest_framework import serializers
from project.models import *
from users.models import *
from task.models import *
from django.contrib.auth.models import User, Group, Permission


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','first_name','last_name','email','username')

class ProfileUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileUser
        fields =('url', 'id','fk_profileUser_user','loadPhoto', 'activationKey','imageProfile', 'phone')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields =('url', 'id','name', 'permissions')

class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields=('url','id','name','content_type_id','codename')

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields=('url','code','name','description','startDate', 'endDate', 'status')

class ProjectUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectUser
        fields=('url','id','project','user','isResponsable')

class DocumentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Documents
        fields = ('url', 'id', 'file', 'fk_documents_project_id', 'description')

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('url', 'code', 'name', 'startDate', 'endDate', 'status',  'project', 'description')

class DependencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dependency
        fields = ('url', 'id', 'dependence', 'task')







