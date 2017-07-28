# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import ProfileUser

# Create your models here.

class Task(models.Model):
	STATUS = (
		('In Progress', 'In Progress'),
		('Technical Review', 'Technical Review'),
		('Functional Review', 'Functional Review'),
		('Customer Acceptance', 'Customer Acceptance')
		)
	code = models.CharField(primary_key = True, max_length=8, blank=False)
	name = models.CharField(max_length = 20, blank=False, unique=True)
	description = models.CharField(max_length=120, blank=True)
	startDate = models.DateField(null=True)
	endDate = models.DateField(null=True)
	status= models.CharField(max_length= 20, choices=STATUS)
	users= models.ForeignKey(ProfileUser, blank=False)
	dependency = models.ForeignKey("Task", blank = True)
