#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from role.forms import *

PHONE_VALIDATOR = RegexValidator(
    regex=r'^(0414|0412|0424|0416|0426)\d{7}$',
    message="Formato de teléfono inválido.",
)

class LoginForm(forms.Form):
	class Meta:
		model = User
		fields = ('username','password','email',)

class UserForm(forms.ModelForm):
	first_name = forms.TextInput(attrs={'id':"first_name",
										'type':"text",
										 'class':"validate",
										'autocomplete':'off'})
	last_name= forms.TextInput(attrs={'id':"last_name",
										'type':"text",
										 'class':"validate",
										'autocomplete':'off'})
	username=forms.CharField(required=True)
	phone = forms.CharField(required=False, validators=[PHONE_VALIDATOR],
							widget=forms.TextInput(attrs={
								'placeholder': "Ej:0412xxxxxx",
								'autocomplete': 'off'}
							))
	email = forms.EmailField(required=True,
							 widget= forms.EmailInput(attrs={'id':"email",
							 	'type':"email",
							 	'class':"validate",
								'autocomplete': 'off'}))

	imageProfile = forms.ImageField(required=False)

	project = forms.CharField(required = False, widget = forms.TextInput(attrs = {'type':"text",
	 								'id':"autocomplete",
	 								 'class':"autocomplete"}))
	rol = forms.ModelChoiceField(
        required=True,
        queryset=Group.objects.all()
    )


	class Meta:
		model= User
		fields = ('first_name','last_name','username','email','groups',)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).count() != 0:
			msj = "Este correo ya está siendo utilizado"
			self.add_error('email', msj)
		return email

class UpdateUserForm(forms.ModelForm):
	first_name = forms.CharField(required = True,
								 widget= forms.TextInput(attrs={'id':"first_name",
										'type':"text",
										 'class':"validate"}))
	last_name= forms.CharField(required=True,
							   widget= forms.TextInput(attrs={'id':"last_name",
										'type':"text",
										 'class':"validate"}))
	username=forms.CharField(required= False)
	phone = forms.CharField(required=False, validators=[PHONE_VALIDATOR],
							widget=forms.TextInput(attrs={
								'placeholder':"Ej:0412xxxxxx"
							}))
	email = forms.EmailField(required=True,
							 widget= forms.EmailInput(attrs={'id':"email",
										'type':"email",
										 'class':"validate"}))

	project = forms.CharField(required = False, widget=forms.TextInput(attrs={'type': "text",
															'id': "autocomplete",
															'class': "autocomplete"}))

	rol = forms.ModelChoiceField(
        required=True,
        queryset=Group.objects.all()
    )

	class Meta:
		model= User
		fields = ('first_name','last_name','email','groups',)
    #
	# def clean_email(self):
	# 	print("Clean email")
	# 	email = self.cleaned_data.get('email')
	# 	if User.objects.filter(email=email).count() != 0:
	# 		print("dentro del if")
	# 		msj = "Este correo ya está siendo utilizado"
	# 		self.add_error('email', msj)
	# 	return email

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
	first_name = forms.CharField(required=True,
								 widget=forms.TextInput(attrs={'id': "first_name",
															   'type': "text",
															   'class': "validate"}))
	last_name = forms.CharField(required=True,
							   widget=forms.TextInput(attrs={'id': "last_name",
															 'type': "text",
															 'class': "validate"}))
	username=forms.CharField(required= True)
	phone = forms.CharField(required=False)
	image_profile = forms.ImageField(required=False)

	class Meta:
		model= User
		fields = ('first_name','last_name','groups',)


