# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from psycopg2._psycopg import Date

from task.forms import *

# Create your views here.


class New_Task(FormView):
	template_name = 'new_work.html'
	form_class = NewTaskForm

	def get_context_data(self, **kwargs):
		context = super(
			New_Task, self).get_context_data(**kwargs)
		print("get")
		project = Project.objects.get(code=self.kwargs['pk'])
		task = Task.objects.filter(project=project)

		context['title'] = 'Agregar'
		context['task'] = task
		return context

	def post(self, request, *args, **kwargs):
		post_values = request.POST.copy()
		print(request.POST['dependencia'])
		form = NewTaskForm(post_values)

		if form.is_valid():
			project=self.kwargs['pk']
			task = form.save(commit=False)
			if (Task.objects.all().count()) == 0:
				task.code = project + '-001'
			else:
				task_all = Task.objects.all()
				key = []
				for i in task_all:
					work = Task.objects.get(name = i)
					key.append (work.code.split('-'))
				temp = []
				arrayKey =[]
				for z in key:
					temp.append(z[0])
				if (temp.count(str(project))) == 0:
					task.code = project + '-001'
				else:
					for k in key:
						if k[0] == str(project):
							arrayKey.append(k)
					arrayKey.sort()
					last = arrayKey.pop()
					newCode = int(last[1]) + 1
					if len(str(newCode)) == 1:
						task.code = project + '-00'+ str(newCode)
					elif len(str(newCode)) == 2:
						task.code = project + '-0'+ str(newCode)
					else:
						task.code = project + '-'+ str(newCode)
			task.project = Project.objects.get(code=project)
			task.name = post_values['name']
			user = post_values['user']
			task.users = ProfileUser.objects.get(id = user)
			a = post_values['startDate'].split('-')
			startDate = a[2]+'-'+a[1]+'-'+a[0]
			task.startDate = startDate
			b = post_values['endDate'].split('-')
			endDate = b[2] + '-' + b[1] + '-' + b[0]
			task.endDate = endDate
			#FALTA LA DEPENDENCIA
			dependence = post_values['dependency']
			print("soy dependencia")
			print(dependence)
			if dependence != '':
				task.dependency=Task.objects.get(code = dependence)
			task.status=post_values['status']
			task.description= post_values['description']
			#task.save()
			return HttpResponseRedirect(reverse_lazy('new_task',
													kwargs={'pk':project}))
		else:
			messages.success(request, "Error al registrar el proyecto")
			return HttpResponseRedirect(reverse_lazy('new_project'))

def Gantt(request):
	project = request.GET.get('project',None)
	project_pk = Project.objects.get(code=project)
	tasks = Task.objects.filter(project=project_pk)
	#print(request.user.id) Con esto obtengo el id user log
	array = []
	for task in tasks:
		#print(task)
		task_pk = Task.objects.get(name = task)
		duration = task.endDate - task.startDate
		array.append([task.code,task.name,task.startDate, task.endDate, duration.days, 100, None ])
	return JsonResponse(array, safe=False)




