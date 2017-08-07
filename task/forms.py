#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import DateField
from task.models import *
from django.db import models


class NewTaskForm(forms.ModelForm):
	status = forms.ChoiceField(
        required=True,
        choices=[
        	('--','---'),
            ('In Progress', 'In Progress'),
			('Technical Review', 'Technical Review'),
			('Functional Review', 'Functional Review'),
			('Customer Acceptance', 'Customer Acceptance')
        ]
    )

	responsable_querySet = User.objects.all()
	print(responsable_querySet)

	users = forms.ModelChoiceField(
		required=True,
		queryset= responsable_querySet,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default",
									
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
	dependencia = forms.CharField(required=False)

	description = forms.CharField(required=False,
								  widget= forms.Textarea(attrs={'class':"materialize-textarea",
										 'id':"textarea",
										 'maxlength':"120",
										 'length':"120"
	 								}))

	# def __init__(self, *args, **kwargs):
	# 	task = kwargs.pop('task', None)
	# 	print(task)

	# 	super(NewTaskForm, self).__init__(*args, **kwargs)

	# 	if task:
	# 		self.fields['dependency'].initial = task[0]['dependency']
	class Meta:
		model = Task
		fields = ('name',)

	def __init__(self, *args, **kwargs):
		self.code = kwargs.pop('code', None)
		super(NewTaskForm, self).__init__(*args, **kwargs)

	def clean_name(self,**kwargs):
		name = self.cleaned_data.get('name')
		if Task.objects.filter(name=name, project=self.code).count() != 0:
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


