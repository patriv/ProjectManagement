#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import DateField

from ProjectManagement import settings
from project.models import *
from  task.models import *
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
		required= True,
		queryset= cliente,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default",

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
		splitEndDate = endDate.split('-')
		startDate = self.cleaned_data.get('startDate')
		splitStartDate = startDate.split('-')
		startDate = datetime.date(int(splitStartDate[2]),int(splitStartDate[1]),int(splitStartDate[0]))
		endDate = datetime.date(int(splitEndDate[2]),int(splitEndDate[1]),int(splitEndDate[0]))
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

class statusForm(forms.ModelForm):
	status = forms.ChoiceField(
		required=True,
		choices=[
			('--', '---'),
			('In Progress', 'In Progress'),
			('Technical Review', 'Technical Review'),
			('Functional Review', 'Functional Review'),
			('Customer Acceptance', 'Customer Acceptance'),
			('Done', 'Done')
		]
	)
	class Meta:
		model=Task
		fields=('status',)

class DocumentsForm(forms.ModelForm):
	class Meta:
		model= Documents
		fields = ('file', 'description',)

class MoreUsersForm(forms.ModelForm):
	class Meta:
		model = ProjectUser
		fields = ('user',)
