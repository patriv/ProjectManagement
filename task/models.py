# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models import ProfileUser
from project.models import Project

class Task(models.Model):
	STATUS = (
		('In Progress', 'In Progress'),
		('Technical Review', 'Technical Review'),
		('Functional Review', 'Functional Review'),
		('Customer Acceptance', 'Customer Acceptance'),
		('Done', 'Done')
		)
	code = models.CharField(primary_key = True, max_length=8, blank=False)
	name = models.CharField(max_length = 20, blank=False)
	description = models.CharField(max_length=120, blank=True)
	startDate = models.DateField(null=True)
	endDate = models.DateField(null=True)
	status= models.CharField(max_length= 20, choices=STATUS)
	users= models.ForeignKey(ProfileUser, blank=False)
	project = models.ForeignKey(Project)
	endDateReal = models.DateField(null= True)
	idTeamWorkTask = models.IntegerField(blank=True, null=True)
	idTaskTW = models.IntegerField(blank=True, null=True)

	class Meta:
		unique_together = ('name','project',)

	def __str__(self):
		return self.name


	def get_startDate(self):
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


class Dependency (models.Model):
	task = models.ForeignKey(Task)
	dependence = models.CharField(max_length=10)

	def __str__(self):
		return self.dependence

