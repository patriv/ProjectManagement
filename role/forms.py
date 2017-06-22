#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group

class RoleForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ('name',)

