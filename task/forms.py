#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.auth.models import User
from task.models import *


class NewTaskForm(forms.ModelForm):
	status = forms.ChoiceField(
        required=True,
        choices=[
        	('--','---'),
            ('In Progress', 'In Progress'),
			('Technical Review', 'Technical Review'),
			('Functional Review', 'Functional Review'),
			('Customer Acceptance', 'Customer Acceptance'),
			('Done', 'Done')
        ]
    )

	responsable_querySet = User.objects.all()

	users = forms.ModelChoiceField(
		required=True,
		queryset= responsable_querySet,
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
	dependencia = forms.CharField(required=False)

	description = forms.CharField(required=False,
								  widget= forms.Textarea(attrs={'class':"materialize-textarea",
										 'id':"textarea",
										 'maxlength':"120",
										 'length':"120"
	 								}))

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
		splitEndDate = endDate.split('-')
		startDate = self.cleaned_data.get('startDate')
		splitStartDate = startDate.split('-')
		startDate = datetime.date(int(splitStartDate[2]),int(splitStartDate[1]),int(splitStartDate[0]))
		endDate = datetime.date(int(splitEndDate[2]),int(splitEndDate[1]),int(splitEndDate[0]))
		if (endDate < startDate):
			msj = "La fecha de culminación no puede ser anterior a la de inicio"
			self.add_error('endDate', msj)
		return endDate


