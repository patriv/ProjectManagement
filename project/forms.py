#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import DateField

from ProjectManagement import settings
from project.models import *
from django.db import models

class NewProjectForm(forms.ModelForm):

	status = forms.ChoiceField(
        required=True,
        choices=[
        	('--','---'),
            ('In Progress', 'In Progress'),
			('Done', 'Done')
        	]
    )

	cliente = User.objects.all().filter(groups__name="Cliente")

	client = forms.ModelChoiceField(
		queryset= cliente,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default",
									'value': "pvalencia"
	})
	)

	company_querySet = User.objects.exclude(groups__name= "Cliente")


	company = forms.ModelChoiceField(
		queryset=company_querySet,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default"
		})
	)

	startDate = forms.CharField(
						   widget= forms.TextInput(attrs={'id':"start",
															  'type':"date",
															  'class':"datepicker"
						   }))

	endDate = forms.CharField(
					   widget=forms.TextInput(attrs={'id': "end",
														 'type': "date",
														 'class': "datepicker"
														 }))

	description = forms.CharField(required=False,
								  widget= forms.Textarea(attrs={'class':"materialize-textarea",
										 'id':"textarea",
										 'maxlength':"120",
										 'length':"120"
	 								}))
	class Meta:
		model = Project
		fields = ('name',)


	def clean_name(self):

		name = self.cleaned_data.get('name')
		if Project.objects.filter(name=name).count() != 0:
			msj = "El nombre de proyecto ya existe, por favor verifique"
			self.add_error('name', msj)
		return name

	def clean_endDate(self):

		endDate = self.cleaned_data.get('endDate')
		startDate = self.cleaned_data.get('startDate')
		if (endDate < startDate):
			msj = "La fecha de culminación no puede ser anterior a la de inicio"
			self.add_error('endDate', msj)
		return endDate


class UpdateProjectForm(forms.ModelForm):

	name = forms.CharField()

	status = forms.ChoiceField(
        required=True,
        choices=[
        	('--','---'),
            ('In Progress', 'In Progress'),
			('Done', 'Done')
        	]
    )

	cliente = User.objects.all().filter(groups__name="Cliente")

	client = forms.ModelChoiceField(
		queryset= cliente,
		required=False,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default",
									'value': "pvalencia"
	})
	)

	company_querySet = User.objects.exclude(groups__name= "Cliente")


	company = forms.ModelChoiceField(
		queryset=company_querySet,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default"
		})
	)

	startDate = forms.CharField(
						   widget= forms.TextInput(attrs={'id':"start",
															  'type':"date",
															  'class':"datepicker"
						   }))

	endDate = forms.CharField(
						   widget= forms.TextInput(
						   	attrs={'id': "end",
						     		 'type': "date",
								 'class': "datepicker"
							 }))

	description = forms.CharField(required=False,
								  widget= forms.Textarea(attrs={'class':"materialize-textarea",
										 'id':"textarea",
										 'maxlength':"120",
										 'length':"120"
	 								}))
	class Meta:
		model = Project
		fields = ('description',)

# class UserForm(forms.ModelForm):
# 	first_name = forms.TextInput(attrs={'id':"first_name",
# 										'type':"text",
# 										 'class':"validate"})
# 	last_name= forms.TextInput(attrs={'id':"last_name",
# 										'type':"text",
# 										 'class':"validate"})
# 	username=forms.TextInput(attrs={'id':"last_name",
# 										'type':"text",
# 										 'class':"validate"})
# 	phone = forms.CharField(required=False)
# 	email = forms.EmailInput(attrs={'id':"email",
# 										'type':"email",
# 										 'class':"validate"})

# 	image_profile = forms.ImageField(required=False)

# 	rol = forms.ModelChoiceField(
#         required=True,
#         queryset=Group.objects.all()
#     )

# 	class Meta:
# 		model= User
# 		fields = ('first_name','last_name','username','email','groups',)

# 	def clean_email(self):
# 		print("Clean email")
# 		email = self.cleaned_data.get('email')
# 		if User.objects.filter(email=email).count() != 0:
# 			print("dentro del if")
# 			msj = "Este correo ya está siendo utilizado"
# 			self.add_error('email', msj)
# 		return email

# class UpdateUserForm(forms.ModelForm):
# 	first_name = forms.CharField(required = True,
# 								 widget= forms.TextInput(attrs={'id':"first_name",
# 										'type':"text",
# 										 'class':"validate"}))
# 	last_name= forms.CharField(required=True,
# 							   widget= forms.TextInput(attrs={'id':"last_name",
# 										'type':"text",
# 										 'class':"validate"}))
# 	username=forms.CharField(required= False)
# 	phone = forms.CharField(required=False)
# 	email = forms.EmailField(required=True,
# 							 widget= forms.EmailInput(attrs={'id':"email",
# 										'type':"email",
# 										 'class':"validate"}))


# 	rol = forms.ModelChoiceField(
#         required=True,
#         queryset=Group.objects.all()
#     )

# 	class Meta:
# 		model= User
# 		fields = ('first_name','last_name','email','groups',)

# class PasswordResetForm(forms.ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ('email',)

# class FirstSessionForm(forms.ModelForm):
# 	password2 = forms.CharField(
# 		label="Repita la Contraseña: ",
# 		widget=forms.PasswordInput()
# 		)

# 	password = forms.CharField(
#     	label="Contraseña: ",
#     	widget=forms.PasswordInput()
#     	)

# 	class Meta:
# 		model = User
# 		fields=['password',]

# 	def clean(self):
# 		password = self.cleaned_data.get('password')
# 		password2 = self.cleaned_data.get('password2')
# 		lenPass = len(password)

# 		if password and password != password2:
# 			msj = "Las contraseñas no coinciden, por favor intente nuevamente."
# 			self.add_error('password',msj)

# 		if (lenPass < 8) or (lenPass >= 16 ):
# 			msj = "La contraseña debe ser mayor a 8 dígitos y menor a 15."
# 			self.add_error('password2',msj)
# 		return self.cleaned_data

# class UpdateProfileForm(forms.ModelForm):
# 	first_name = forms.CharField(required=True,
# 								 widget=forms.TextInput(attrs={'id': "first_name",
# 															   'type': "text",
# 															   'class': "validate"}))
# 	last_name = forms.CharField(required=True,
# 							   widget=forms.TextInput(attrs={'id': "last_name",
# 															 'type': "text",
# 															 'class': "validate"}))
# 	username=forms.CharField(required= True)
# 	phone = forms.CharField(required=False)
# 	image_profile = forms.ImageField(required=False)

# 	class Meta:
# 		model= User
# 		fields = ('first_name','last_name','groups',)
