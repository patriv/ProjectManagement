#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from project.models import profileUser


class LoginForm(forms.Form):
	class Meta:
		model = User
		fields = ('username','password','email',)

class UserForm(forms.ModelForm):
	first_name = forms.CharField()
	last_name= forms.CharField()
	username=forms.CharField()
	phone = forms.CharField(required=False)
	email = forms.EmailField()
	class Meta:
		model= User
		fields = ('first_name','last_name','username','email')

class ProfileForm(forms.ModelForm):
	class Meta:
		model=profileUser
		fields=('user','role',)