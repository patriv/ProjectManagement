# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.auth.models import User,Group
from django.db import models

# Create your models here.


class Project(models.Model):
	STATUS = (
		('In Progress', 'In Progress'),
		('Technical Review', 'Technical Review'),
		('Functional Review', 'Functional Review'),
		('Customer Accepance','Customer Acceptance')
		)

	code = models.CharField(primary_key = True, max_length=8, blank=False)
	name = models.CharField(max_length = 20, blank=False)
	description = models.CharField(max_length=120, blank=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	status= models.CharField(max_length= 10, choices=STATUS)
	
class Documents(models.Model):
	file = models.FileField(upload_to='files/')
	id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
