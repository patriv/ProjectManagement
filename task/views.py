# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from psycopg2._psycopg import Date

from google_calendar import create_event
from project.models import ProjectUser
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
        context['code'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = NewTaskForm(post_values, code=self.kwargs['pk'])

        if form.is_valid():
            project=self.kwargs['pk']
            project_pk=Project.objects.get(code=project)
            task = form.save(commit=False)
            if (Task.objects.all().count()) == 0:
                task.code = project + '-001'
            else:
                task_all= Task.objects.filter(project=project)
                if task_all.count() == 0:
                    print("soy vacio")
                    task.code = project + '-001'
                else:
                    key = []
                    print("hello")
                    print(task_all)
                    for i in task_all:
                        key.append(i.code.split('-'))
                    print("soy key")
                    print(key)
                    key.sort()
                    last = key.pop()
                    newCode = int(last[1]) + 1
                    print(newCode)
                    if len(str(newCode)) == 1:
                        task.code = project + '-00'+ str(newCode)
                    elif len(str(newCode)) == 2:
                        task.code = project + '-0'+ str(newCode)
                    else:
                        task.code = project + '-'+ str(newCode)

            task.project = Project.objects.get(code=project)
            task.name = post_values['name']
            user = post_values['users']
            print(user)
            task.users = ProfileUser.objects.get(id = user)
            print(task.users)
            projectUser = ProjectUser.objects.filter(user=task.users).count()
            print(projectUser)
            if projectUser == 0:
                newRelation= ProjectUser(isResponsable=False, project=task.project, user_id=task.users.pk)
                newRelation.save()
            responsable = ProjectUser.objects.get(project=project_pk, isResponsable=True)
            print("RESPONSABLEEE " +str(responsable.user.fk_profileUser_user.email))
            print(task.users.fk_profileUser_user.email)
            a = post_values['startDate'].split('-')
            startDate = a[2]+'-'+a[1]+'-'+a[0]
            task.startDate = startDate
            b = post_values['endDate'].split('-')
            endDate = b[2] + '-' + b[1] + '-' + b[0]
            task.endDate = endDate
            task.status=post_values['status']
            task.description= post_values['description']

            # Se crea el evento para realizar la conexión con Google Calendar

            tz = pytz.timezone('America/Caracas')
            print(tz)
            start_datetime = tz.localize(datetime.datetime(int(a[2]), int(a[1]), int(a[0])))
            print(start_datetime)
            stop_datetime = tz.localize(datetime.datetime(int(b[2]), int(b[1]), int(b[0])))
            print(stop_datetime)
            event = {
                'summary': 'Tarea ' + str(task.name)+" del proyecto "+str(project_pk.name),
                'description': task.description,
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'America/Caracas',
                },
                'end': {
                    'dateTime': stop_datetime.isoformat(),
                    'timeZone': 'America/Caracas',
                },
                'attendees': [
                    {'email': task.users.fk_profileUser_user.email},
                    {'email': responsable.user.fk_profileUser_user.email},
                ],
            }

            create_event(event)
            print("se creo el evento")

            ####################################################

            task.save()
            #FALTA LA DEPENDENCIA
            dependence = post_values['dependencia']
            if dependence != '':
                dependences = dependence.split(',')
                print("soy dependencia")
                print(dependence)
                task_save = Task.objects.get(code = task.code)

                for i in dependences:
                    if i != '':
                        print(i)
                        c = Task.objects.get(project=task.project, name = i)
                        print(c)
                        task_dependence = Dependency(task = task_save, dependence=c.code)
                        task_dependence.save()


            messages.success(request, "La tarea se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('new_task',
                                                    kwargs={'pk':project}))
        else:
            messages.success(request, "Error al registrar la tarea")
            return render(request, 'new_work.html', {'form': form, 'pk': self.kwargs['pk']})


def Gantt(request):
    project = request.GET.get('project',None)
    project_pk = Project.objects.get(code=project)
    tasks = Task.objects.filter(project=project_pk)
    print(tasks)
    #print(request.user.id) Con esto obtengo el id user log
    array = []
    for task in tasks:
        duration = task.endDate - task.startDate
        print(task.code)
        array.append([task.code,task.name,task.startDate, task.endDate, duration.days, 100, None ])
    print(array)
    return JsonResponse(array, safe=False)

class Update_Task(TemplateView):
    template_name = 'new_work.html'
    form_class = NewTaskForm

    def get_context_data(self, **kwargs):
            context = super(
                Update_Task, self).get_context_data(**kwargs)
            print("get de update tareas")
            context['title'] = 'Modificar'
            task_pk = Task.objects.get(code = self.kwargs['code'])
            print(task_pk.project.code)
            task = Task.objects.filter(project=task_pk.project.code)
            if task_pk.startDate == None:
                startDate = ''
            else:
                startDate = task_pk.startDate.strftime("%d-%m-%Y")
            if task_pk.endDate == None:
                endDate = ''
            else:
                endDate = task_pk.endDate.strftime("%d-%m-%Y")
            dependence = Dependency.objects.filter(task=task_pk)
            print(dependence)
            z = []
            for i in dependence:
                tarea = Task.objects.get(code = i)
                z.append(tarea.name)


            data = {'name': task_pk,
                    'users': task_pk.users.fk_profileUser_user,
                    'startDate': startDate,
                    'endDate': endDate,
                    'status': task_pk.status,
                    'description': task_pk.description
                    }

            form = NewTaskForm(initial=data)
            context['form'] = form
            context['task'] = task
            context['dependencia'] = z
            return context

    def post(self, request, *args, **kwargs):
        print("post de update tareas")
        post_values = request.POST.copy()
        form = NewTaskForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            task_pk = self.kwargs['code']
            task = Task.objects.get(code = task_pk)

            print(task.project)
            task.name = post_values['name']
            profile_users = post_values['users']
            task.users = ProfileUser.objects.get(fk_profileUser_user=profile_users)

            a = post_values['startDate'].split('-')
            startDate = a[2]+'-'+a[1]+'-'+a[0]
            print(startDate)
            task.startDate =startDate
            b = post_values['endDate'].split('-')
            endDate = b[2]+'-'+b[1]+'-'+b[0]
            task.endDate = endDate
            #FALTA DEPENDENCIA
            dependency = Dependency.objects.filter(task=task)
            print(dependency)
            dependence = post_values['dependencia']
            print("soy yo")
            print(dependence)
            dependence = dependence.split(',')
            print(dependence)

            array_dependece = []
            for a in dependency:
                array_dependece.append(Task.objects.get(code = a.dependence).name)
                print(a.dependence)
            print(array_dependece)
            for x in array_dependece:
                print(x)
                count_exist = dependence.count(x)
                print(count_exist)
                if count_exist == 0:
                    a = Task.objects.get(name=x).code
                    delete_dependence = Dependency.objects.get(dependence=a, task = task)
                    delete_dependence.delete()

            for d in dependence:
                print("soy d")
                print(d)
                if d != '':
                    code = Task.objects.get(name=d)
                    print(code)
                    dependency = Dependency.objects.filter(dependence=code.code,task=task).exists()
                    print(dependency)
                    if not dependency:
                        print("dentro de dependency")
                        new = Dependency(dependence=code.code,task=task)
                        new.save()

            # la dependencia esta mala!
            task.status = post_values['status']
            task.description = post_values['description']
            task.save()


            messages.success(request, "La tarea ha sido modificada exitosamente")
            return HttpResponseRedirect(reverse_lazy('detail_project',
                                                kwargs={'pk': task.project.code}))
        else:
            return render(request, 'new_work.html', {'form':form, 'code':self.kwargs['code']})

def ValidateTask(request):
    print("*********** en validate************")
    name = request.GET.get('name', None)
    print(name)
    code = request.GET.get('code', None)
    print(code)
    data = {
        'name_exists': Task.objects.filter(name=name, project=code).exists()
    }

    return JsonResponse(data)

def DeleteTask(request,code):
    print("delete")
    task = Task.objects.get(code=code)
    project = Project.objects.get(code=task.project.code)
    print(task.project.code)

    if task.status == 'Technical Review':
        messages.success(request, "La tarea " + str(task.name) + " no se puede eliminar.")
        return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": task.project.code}))
    else:
        task.delete()
        messages.success(request, "La tarea " + str(task.name) + " se ha eliminado exitosamente")
        return HttpResponseRedirect(reverse_lazy('detail_project',kwargs={"pk":task.project.code}))


def DetailTask(request, code):
    print("*********** en validate task************")
    code = request.GET.get('code', None)
    print(code)
    data = {
        'name_exists': Task.objects.filter(code=code).exists()
    }

    task = Task.objects.get(code=code)
    data['name']=task.name
    data['responsable']=task.users.fk_profileUser_user.first_name+" "+task.users.fk_profileUser_user.last_name
    data['status']= task.status
    data['description']=task.description

    return JsonResponse(data)









