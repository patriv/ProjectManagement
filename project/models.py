# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.contrib.auth.models import User,Group
from django.db import models
from users.models import ProfileUser

# Create your models here.


class Project(models.Model):
	STATUS = (
		('In Progress', 'In Progress'),
		('Done', 'Done')
		)

	code = models.CharField(primary_key = True, max_length=8, blank=False, unique=True)
	name = models.CharField(max_length = 20, blank=False, unique=True)
	description = models.CharField(max_length=120, blank=True)
	startDate = models.DateField(null=True)
	endDate = models.DateField(null=True)
	status= models.CharField(max_length= 20, choices=STATUS)
	users= models.ManyToManyField(ProfileUser, through='ProjectUser')
	idTeamWorkProject = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.name

	def get_startDate(self):
		print("holis")
		formato = "%d-%m-%Y"
		if self.startDate is None:
			return ''

		date_time = self.startDate.strftime(formato)

		return date_time

	def get_endDate(self):
		formato = "%d-%m-%Y"
		if self.endDate is None:
			return ''

		date_time = self.endDate.strftime(formato)

		return date_time

class ProjectUser(models.Model):
	user = models.ForeignKey(ProfileUser)
	project = models.ForeignKey(Project)
	isResponsable = models.BooleanField(default=False)

	def __str__(self):
		return self.project.code


class Documents(models.Model):
	file = models.FileField(upload_to='files/')
	fk_documents_project = models.ForeignKey(Project, on_delete=models.CASCADE)
	description = models.CharField(max_length=64, blank=False)

	def __str__(self):
		return self.fk_documents_project.name
