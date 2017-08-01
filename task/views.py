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
		print("en post task")
		post_values = request.POST.copy()
		form = NewTaskForm(post_values)
		print(form.is_valid())
		print(form)
		if form.is_valid():
			project=self.kwargs['pk']
			print(project)
			task = form.save(commit=False)
			print(Task.objects.all().count())
			if (Task.objects.all().count()) == 0:
				task.code = project + '-001'
			else:
				print("no es el primero")
				sequence = Task.objects.all().order_by("-code")[0].code
				print(sequence)
				sequenceSplit = sequence.split('-')
				print(sequenceSplit)
				sequenceNum = int(sequenceSplit[1]) + 1

				if len(str(sequenceNum)) == 1:
					task.code = project + '-00'+ str(sequenceNum)
				elif len(str(sequenceNum)) == 2:
					task.code = project + '-0'+str(sequenceNum)
				else:
					task.code = project + '-'+str(sequenceNum)
				print(task.code)

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
			print(dependence)
			if dependence != '':
				task.dependency=Task.objects.get(code = dependence)
				print(task.dependency)
			task.status=post_values['status']
			task.description= post_values['description']
			print(task.users)
			task.save()
			return HttpResponseRedirect(reverse_lazy('new_task',
													kwargs={'pk':project}))
		else:
			messages.success(request, "Error al registrar el proyecto")
			return HttpResponseRedirect(reverse_lazy('new_project'))

def Gantt(request):
	project = request.GET.get('project',None)
	print(project)


	project_pk = Project.objects.get(code=project)
	print(project_pk.code)
	tasks = Task.objects.filter(project=project_pk)
	print(tasks)
	#print(request.user.id) Con esto obtengo el id user log
	array = []
	for task in tasks:
		#print(task)
		task_pk = Task.objects.get(name = task)
		duration = task.endDate - task.startDate
		print(duration.days)
		print(type(task.endDate))
		array.append([task.code,task.name,task.startDate, task.endDate, duration.days, 100, None ])
		print(task_pk.code)

	# array = ([
	# 	['Proyecto', 'Estimada', 'Real']
	# ])

	# x =[p.name for p in proj]
	# duration = []
	# for i in x:
	# 	project = Project.objects.get(name=i)
	# 	print(project)
	# 	tasksCount = Task.objects.filter(project_id=project.code).count()
	# 	if tasksCount == 0:
	# 		days = 0
	# 		array.append([i,days,100])
	# 	else:
	# 		tasks = Task.objects.filter(project_id=project.code)
	# 		print("soy tareas" + str(tasks))
	# 		for task in tasks:
	# 			print(task)
	# 			days = task.endDate - task.startDate
	# 			print("soy los dias "+str(days.days))
	# 			print(duration)
	# 			duration.append(days.days)
	# 		days=sum(duration)
	# 		array.append([project.name,days,100])
	# 		duration = []

	# 		print(duration)

	print(array)


	return JsonResponse(array, safe=False)




