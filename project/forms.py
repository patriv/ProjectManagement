#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
	class Meta:
		model = User
		fields = ('username','password','email',)

class RoleForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ('name',)

