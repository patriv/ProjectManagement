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

	image_profile = forms.ImageField(required=False)

	rol = forms.ModelChoiceField(
        required=True,
        queryset=Group.objects.all()
    )

	class Meta:
		model= User
		fields = ('first_name','last_name','username','email','groups',)

	def clean_email(self):
		print("Clean email")
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).count() != 0:
			print("dentro del if")
			msj = "Este correo ya está siendo utilizado"
			self.add_error('email', msj)
		return email

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

class PasswordResetForm(forms.ModelForm):
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

	def clean(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		lenPass = len(password)

		if password and password != password2:
			msj = "Las contraseñas no coinciden, por favor intente nuevamente."
			self.add_error('password',msj)

		if (lenPass < 8) or (lenPass >= 16 ):
			msj = "La contraseña debe ser mayor a 8 dígitos y menor a 15."
			self.add_error('password2',msj)
		return self.cleaned_data

class UpdateProfileForm(forms.ModelForm):
	first_name = forms.TextInput(attrs={'id':"first_name",
										'type':"text",
										 'class':"validate"})
	last_name= forms.TextInput(attrs={'id':"last_name",
										'type':"text",
										 'class':"validate"})
	#username=forms.CharField(required= False)
	phone = forms.CharField(required=False)
	image_profile = forms.ImageField(required=False)

	class Meta:
		model= User
		fields = ('first_name','last_name','groups',)


		# def clean_username(self):
# 		username = self.cleaned_data.get('username')
# 		if User.objects.filter(username=username).count() != 0:
# 			raise forms.ValidationError(u'Este nombre de usuario ya está siendo utilizado.')
# 		return username
#
#
#
#
# 	def save(self, commit=True):
# 		user = super(UserForm, self).save(commit=False)
# 		user.email = self.cleaned_data['email']
# 		user.username = self.cleaned_data['username']
# 		user.first_name = self.cleaned_data['first_name']
# 		user.last_name = self.cleaned_data['last_name']
# 		user.is_active = 1
# 		password = self.cleaned_data['passw']
# 		user.set_password(password)
# 		user.save()
# return user