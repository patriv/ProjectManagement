from rest_framework import serializers
from users.models import *
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
        fields =('url', 'id','name')

class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields=('url','id','name','content_type_id','codename')

class GroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group.permissions
        fields=('url','id','group_id','permission_id')



