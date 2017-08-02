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

	user = forms.ModelChoiceField(
		queryset= responsable_querySet,
		widget=forms.Select(attrs={'id':"drop",
								   'tabindex' : "1",
									'class' : "chosen-select browser-default",
									'value': "pvalencia"
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
	dependence_querySet = Task.objects.all()


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
		fields = ('name','dependency',)
		widgets = {'dependency':forms.Select(attrs={'multiple':''})}
