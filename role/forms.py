#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group

class RoleForm(forms.ModelForm):
	project = forms.BooleanField(required=False)
	users = forms.BooleanField(required=False)
	rol = forms.BooleanField(required=False)
	view = forms.BooleanField(required=False)
	create = forms.BooleanField(required=False)
	update = forms.BooleanField(required=False)
	delete = forms.BooleanField(required=False)

	class Meta:
		model = Group
		fields = ('name',)

