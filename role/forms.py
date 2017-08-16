#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group

class RoleForm(forms.ModelForm):

	name = forms.CharField(required=False)
	# Project
	create_project = forms.BooleanField(required=False)
	update_project = forms.BooleanField(required=False)
	view_project = forms.BooleanField(required=False)
	delete_project = forms.BooleanField(required=False)
	#Users
	create_users = forms.BooleanField(required=False)
	update_users = forms.BooleanField(required=False)
	view_users = forms.BooleanField(required=False)
	delete_users = forms.BooleanField(required=False)
	#Rol
	create_rol = forms.BooleanField(required=False)
	#view_rol = forms.BooleanField(required=False)
	updtae_rol = forms.BooleanField(required=False)
	delte_rol = forms.BooleanField(required=False)

	class Meta:
		model = Group
		fields = ('id',)

	def clean_name(self,**kwargs):
		name = self.cleaned_data.get('name')
		if Group.objects.filter(name=name).count() != 0:
			msj = "El nombre del rol ya existe, por favor verifique"
			self.add_error('name', msj)
		return name





