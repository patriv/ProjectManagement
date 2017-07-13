# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.auth.models import User,Group
from django.db import models
from users.models import profileUser

# Create your models here.


class Project(models.Model):
	STATUS = (
		('In Progress', 'In Progress'),
		('Done', 'Done')
		)

	code = models.CharField(primary_key = True, max_length=8, blank=False)
	name = models.CharField(max_length = 20, blank=False)
	description = models.CharField(max_length=120, blank=True)
	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	status= models.CharField(max_length= 20, choices=STATUS)
	users= models.ManyToManyField(profileUser, through='Project_user')

	def __str__(self):
		return self.name

class Project_user(models.Model):
	user = models.ForeignKey(profileUser)
	project = models.ForeignKey(Project)
	is_resp = models.BooleanField(default=False)

	def __str__(self):
		return self.project.code



class Documents(models.Model):
	file = models.FileField(upload_to='files/')
	id_project = models.ForeignKey(Project, on_delete=models.CASCADE)
