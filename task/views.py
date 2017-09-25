# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from google_calendar import create_event
from project.models import ProjectUser
from task.forms import *
from newListTaskTW import NewTaskList
from task_TW import AddTask, UpdateTaskTW, DeleteTaskTW

# Create your views here.

'''
Clase que agrega una nueva tarea a un proyecto determinado.
'''
class New_Task(FormView):
    template_name = 'new_work.html'
    form_class = NewTaskForm

    def get_context_data(self, **kwargs):
        context = super(
            New_Task, self).get_context_data(**kwargs)
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
            '''
            Si es la primera tarea que se crea, se le asigna el código del proyecto más el número que indica que es
            la primera.
            '''
            if (Task.objects.all().count()) == 0:
                task.code = project + '-001'
                id_TeamWork=NewTaskList("Tareas "+str(project_pk.name), project_pk.idTeamWorkProject, project_pk.name)
                task.idTeamWorkTask = id_TeamWork
            else:
                task_all= Task.objects.filter(project=project)
                '''
                Si es la primera tarea de un determinado proyecto, se le asigna el código del proyecto más el número que indica 
                que es la primera tarea de ese proyecto.
                '''
                if task_all.count() == 0:
                    task.code = project + '-001'
                    ''''
                    Se crea la nueva lista de tareas en Team Work. Por cada proyecto, inicialmente se crea una sola lista.
                    con el nombre "Tareas NOMBRE DEL PROYECTO"
                    '''
                    id_TeamWork=NewTaskList("Tareas " + str(project_pk.name), str(project_pk.idTeamWorkProject), project_pk.name)
                    task.idTeamWorkTask=id_TeamWork
                else:
                    '''
                    En caso de que no sea la primera tarea, se almacena el codigo de la tarea en un arreglo
                    '''
                    key = []
                    teamWork = 0
                    for i in task_all:
                        key.append(i.code.split('-'))
                        print(key)
                        teamWork=i.idTeamWorkTask #En la variable TeamWork se almacena el id de la lista de tareas de team
                                                  # work, con la finalidad de que todas las tareas tengan esa sola lista
                    key.sort() # Se ordena la lista que contiene todas las tareas del proyecto, con la finalidad de continuar
                               # el orden del código
                    last = key.pop() # Se extrae el útlimo elemento de la lista
                    newCode = int(last[1]) + 1 #El nuevo codigo será el último de la fila +1
                    '''
                    A continuación se crea un patrón para el código para almacenar en la base de datos
                    '''
                    if len(str(newCode)) == 1:
                        task.code = project + '-00'+ str(newCode)
                    elif len(str(newCode)) == 2:
                        task.code = project + '-0'+ str(newCode)
                    else:
                        task.code = project + '-'+ str(newCode)
                    '''
                    Se le asigna a la tarea el id de las listas de team work
                    '''
                    task.idTeamWorkTask=teamWork
            task.project = Project.objects.get(code=project)
            task.name = post_values['name']
            user = post_values['users']
            task.users = ProfileUser.objects.get(id = user)
            '''
            Se comprueba que el usuario que se esté asociando a la tarea, esté igualmente asociado al proyecto al cual pertenece la 
            tarea. En caso de que el ususario no esté asociado con el proyecto de la tarea, se asocia al usuario con este proyecto.
            '''
            projectUser = ProjectUser.objects.filter(user=task.users).count()
            if projectUser == 0:
                newRelation= ProjectUser(isResponsable=False, project=task.project, user_id=task.users.pk)
                newRelation.save()
            responsable = ProjectUser.objects.get(project=project_pk, isResponsable=True)
            '''
            Esta conversión de fechas se hace con la finalidad de guardarlo según el formato que permite PostgreSQL
            '''
            a = post_values['startDate'].split('-')
            startDate = a[2] + '-' + a[1] + '-' + a[0]
            task.startDate = startDate
            b = post_values['endDate'].split('-')
            endDate = b[2] + '-' + b[1] + '-' + b[0]
            task.endDate = endDate
            '''
            Se comprueba que la fecha de inicio o fin de las tareas estén dentro del rango de las fechas de inicio y
            culminación del proyecto.
            '''
            if datetime.date(int(a[2]),int(a[1]),int(a[0])) > project_pk.endDate or datetime.date\
                        (int(b[2]),int(b[1]),int(b[0])) > project_pk.endDate :
                messages.success(request, "El proyecto " +str(project_pk.name)+" finaliza el "
                                 +str(project_pk.endDate.day)+'-'+str(project_pk.endDate.month)+'-'+
                                 str(project_pk.endDate.year)+" , por favor revise las fechas de la tarea")
                return render(request, 'new_work.html', {'form': form, 'pk': self.kwargs['pk']})

            if datetime.date(int(a[2]),int(a[1]),int(a[0])) < project_pk.startDate or \
                            datetime.date(int(b[2]),int(b[1]),int(b[0])) < project_pk.startDate :
                messages.success(request, "El proyecto " +str(project_pk.name)+" inicia el "
                                 +str(project_pk.startDate.day)+'-'+str(project_pk.startDate.month)+'-'+
                                 str(project_pk.startDate.year)+" , por favor revise las fechas de la tarea")
                return render(request, 'new_work.html', {'form': form, 'pk': self.kwargs['pk']})

            task.status=post_values['status']
            task.description= post_values['description']

            '''
            Se crea el evento para realizar la conexión con Google Calendar
            '''
            tz = pytz.timezone('America/Caracas')
            start_datetime = tz.localize(datetime.datetime(int(a[2]), int(a[1]), int(a[0])))
            stop_datetime = tz.localize(datetime.datetime(int(b[2]), int(b[1]), int(b[0])))
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
            ####################################################

            task.save()
            task = Task.objects.get(code=task.code)
            startDate= str(task.startDate).split('-')
            endDate=str(task.endDate).split('-')
            endDate=str(task.endDate).split('-')
            task.idTaskTW=AddTask(task.idTeamWorkTask, task.name, ''.join(startDate), ''.join(endDate))
            task.save()
            '''
            Como la entrada de las dependencias es un string con ',' se guardan en una lista.
            '''
            dependence = post_values['dependencia']
            if dependence != '':
                dependences = dependence.split(',')
                task_save = Task.objects.get(code = task.code)
                '''
                Se guardan cada una de las tareas que dependen de la que se está creando.
                '''
                for i in dependences:
                    if i != '':
                        c = Task.objects.get(project=task.project, name = i)
                        task_dependence = Dependency(task = task_save, dependence=c.code)
                        task_dependence.save()
            messages.success(request, "La tarea se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('new_task',
                                                    kwargs={'pk':project}))
        else:
            messages.success(request, "Error al registrar la tarea")
            return render(request, 'new_work.html', {'form': form, 'pk': self.kwargs['pk']})

'''
Función que envía los datos necesarios al JS para crear el diagrama de Gantt.
'''
def Gantt(request):
    project = request.GET.get('project',None)
    project_pk = Project.objects.get(code=project)
    tasks = Task.objects.filter(project=project_pk)
    array = []
    percent=0
    for task in tasks:
        duration = task.endDate - task.startDate
        '''
        Para determinar el porcentaje de las tareas, se calcula dependiendo del status en que ésta se encuentre.
        Variando de 20% en 20%.
        '''
        if task.status == 'Done':
            percent=100
        elif task.status == 'In Progress':
          percent = 20
        elif task.status == 'Technical Review':
            percent = 40
        elif task.status == 'Functional Review':
            percent = 60
        elif task.status == 'Customer Acceptance':
            percent = 80
        array.append([task.code,task.name,task.startDate, task.endDate, duration.days, percent, None ])
    return JsonResponse(array, safe=False)

'''
Clase que edita una tarea.
'''
class Update_Task(TemplateView):
    template_name = 'new_work.html'
    form_class = NewTaskForm

    def get_context_data(self, **kwargs):
            context = super(
                Update_Task, self).get_context_data(**kwargs)
            context['title'] = 'Modificar'
            task_pk = Task.objects.get(code = self.kwargs['code'])
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
        post_values = request.POST.copy()
        form = NewTaskForm(post_values)

        if form.is_valid():
            task_pk = self.kwargs['code']
            task = Task.objects.get(code = task_pk)
            task.name = post_values['name']
            profile_users = post_values['users']
            task.users = ProfileUser.objects.get(fk_profileUser_user=profile_users)
            '''
            Las fechas son cambiadas al formato de PostgreSQL
            '''
            a = post_values['startDate'].split('-')
            startDate = a[2]+'-'+a[1]+'-'+a[0]
            task.startDate =startDate
            b = post_values['endDate'].split('-')
            endDate = b[2]+'-'+b[1]+'-'+b[0]
            task.endDate = endDate

            '''
            Se guardan las dependencias introducidas por el usuario en un arrelgo.
            '''
            dependence = post_values['dependencia']
            dependence = dependence.split(',')
            array_dependece = []
            '''
            Se ven las tareas dependientes que se tenian antes del update
            '''
            dependency = Dependency.objects.filter(task=task)
            for a in dependency:
                array_dependece.append(Task.objects.get(code = a.dependence).name)
            for x in array_dependece:
                '''
                Se pregunta si existe la tarea que se tenía anterirormente asociada con las modificaciones realizadas
                por el usuario.
                '''
                count_exist = dependence.count(x)
                '''
                Si no existe, se elimina la relación entre las tareas.
                '''
                if count_exist == 0:
                    a = Task.objects.get(name=x).code
                    delete_dependence = Dependency.objects.get(dependence=a, task = task)
                    delete_dependence.delete()

            '''
            En caso de haber una nueva dependencia de tarea que anteriromente no existía, se crea la relación entre ellas.
            '''
            for d in dependence:
                if d != '':
                    code = Task.objects.get(name=d)
                    dependency = Dependency.objects.filter(dependence=code.code,task=task).exists()
                    if not dependency:
                        new = Dependency(dependence=code.code,task=task)
                        new.save()

            task.status = post_values['status']
            task.description = post_values['description']
            task.save()

            '''
            Se realizan conversiones de fechas para que sean guardados en teamwork 
            '''
            task = Task.objects.get(code=task.code)
            startDate = str(task.startDate).split('-')
            endDate = str(task.endDate).split('-')
            print(''.join(startDate))
            '''
            Función que facilita la conexión con TeamWork.
            '''
            UpdateTaskTW(task.idTaskTW, task.name, ''.join(startDate), ''.join(endDate))

            messages.success(request, "La tarea ha sido modificada exitosamente")
            return HttpResponseRedirect(reverse_lazy('detail_project',
                                                kwargs={'pk': task.project.code}))
        else:
            return render(request, 'new_work.html', {'form':form, 'code':self.kwargs['code']})

'''
Función que permite la validación de tareas, y es pasado en formato JSON a un JS.
'''
def ValidateTask(request):
    name = request.GET.get('name', None)
    code = request.GET.get('code', None)
    data = {
        'name_exists': Task.objects.filter(name=name, project=code).exists()
    }

    return JsonResponse(data)

'''
Función que permite la eliminación de una tarea.
@:param code: código de la tarea a eliminar.
'''
def DeleteTask(request,code):
    task = Task.objects.get(code=code)
    project = Project.objects.get(code=task.project.code)

    if task.status == 'Technical Review':
        messages.success(request, "La tarea " + str(task.name) + " no se puede eliminar.")
        return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": task.project.code}))
    else:
        print(task.idTaskTW)
        DeleteTaskTW(task.idTaskTW)
        task.delete()
        messages.success(request, "La tarea " + str(task.name) + " se ha eliminado exitosamente")
        return HttpResponseRedirect(reverse_lazy('detail_project',kwargs={"pk":task.project.code}))

'''
Función que permite enviar mediante un JSON los detalles de una tarea a un JS.
'''
def DetailTask(request, code):
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









