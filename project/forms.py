#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from project.models import profileUser
from django.db import models
from role.forms import *


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
	group=Group.objects.all()
	new=[]
	for i in group:
		new.append((i.id,i.name))
	print(new)

	rol = forms.ChoiceField(
        required=True,
        choices=new
    )
	class Meta:
		model= User
		fields = ('first_name','last_name','username','email')

class FirstSessionForm(forms.ModelForm):
	password2 = forms.CharField(
		label="Repita la Contraseña: ",
		widget=forms.PasswordInput()
		)

	password = forms.CharField(
    	label="Contraseña: ",
    	widget=forms.PasswordInput()
    	)

	class Meta:
		model = User
		fields=['password',]
		
