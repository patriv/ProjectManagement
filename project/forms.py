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
	first_name = forms.TextInput(attrs={'id':"first_name",
										'type':"text",
										 'class':"validate"})
	last_name= forms.TextInput(attrs={'id':"last_name",
										'type':"text",
										 'class':"validate"})
	username=forms.TextInput(attrs={'id':"last_name",
										'type':"text",
										 'class':"validate"})
	phone = forms.CharField(required=False)
	email = forms.EmailInput(attrs={'id':"email",
										'type':"email",
										 'class':"validate"})


	rol = forms.ModelChoiceField(
        required=True,
        queryset=Group.objects.all()
    )

	class Meta:
		model= User
		fields = ('first_name','last_name','username','email','groups',)


class UpdateUserForm(forms.ModelForm):
	first_name = forms.TextInput(attrs={'id':"first_name",
										'type':"text",
										 'class':"validate"})
	last_name= forms.TextInput(attrs={'id':"last_name",
										'type':"text",
										 'class':"validate"})
	username=forms.CharField(required= False)
	phone = forms.CharField(required=False)
	email = forms.EmailInput(attrs={'id':"email",
										'type':"email",
										 'class':"validate"})


	rol = forms.ModelChoiceField(
        required=True,
        queryset=Group.objects.all()
    )

	class Meta:
		model= User
		fields = ('first_name','last_name','email','groups',)

class ForgotPasswordForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email',)

	

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
		
