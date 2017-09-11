# -*- coding: utf-8 -*-
import hashlib
import random
import json
import datetime

import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import *
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from rest_framework.decorators import api_view

from google_drive import upload_file
from google_calendar import create_event
from project.forms import *
from project.models import *
from task.models import *
from django.urls import reverse
from users.views import send_email
from project_TW import add_project, UpdateProjectTW, DeleteProjectTW

'''
Clase que muestra todos los proyectos.
'''
class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(
            Home, self).get_context_data(**kwargs)
        project = Project.objects.all()
        context['project'] = project
        return context

'''
Clase que permite la creación de un nueco proyecto.
'''
class New_Project(FormView):
    template_name = 'page-new-project.html'
    form_class = NewProjectForm

    def get_context_data(self, **kwargs):
        context = super(
            New_Project, self).get_context_data(**kwargs)
        context['title'] = 'Agregar'
        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = NewProjectForm(post_values)
        if form.is_valid():
            project = form.save(commit=False)
            project.name = post_values['name']
            '''
            Se genera un código aleatorio a partir del nombre del proyecto.
            '''
            code = codeProject(project.name)
            code_exist = Project.objects.filter(code=code).exists()
            '''
            Si el código del proyecto existe, se agrega el caracter siguiente del nombre del proyecto.
            '''
            if code_exist:
                length = len(code)
                code = code + project.name[length]
                project.code=code
            else:
                project.code = code
            '''
            Se transforma el formato de las fechas a como las guarda PostgreSQL.    
            '''
            a = post_values['startDate'].split('-')
            startDate = a[2]+'-'+a[1]+'-'+a[0]
            project.startDate = startDate
            b = post_values['endDate'].split('-')
            endDate = b[2] + '-' + b[1] + '-' + b[0]
            project.endDate = endDate
            project.status = post_values['status']
            project.description = post_values['description']
            auth_cliente = post_values['client']
            auth_emp = post_values['company']
            # id de responsable de la empresa
            profile_emp = ProfileUser.objects.get(fk_profileUser_user_id = auth_emp)
            # id del cliente
            profile_client = ProfileUser.objects.get(fk_profileUser_user = auth_cliente)

            # Se crea el evento para realizar la conexión con Google Calendar

            tz = pytz.timezone('America/Caracas')
            start_datetime = tz.localize(datetime.datetime(int(a[2]), int(a[1]), int(a[0])))
            stop_datetime = tz.localize(datetime.datetime(int(b[2]), int(b[1]), int(b[0])))
            event = {
                'summary': 'Proyecto '+ str(project.name),
                'description': project.description,
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'America/Caracas',
                },
                'end': {
                    'dateTime': stop_datetime.isoformat(),
                    'timeZone': 'America/Caracas',
                },
                'attendees': [
                    {'email': profile_emp.fk_profileUser_user.email},
                    {'email': profile_client.fk_profileUser_user.email},
                ],
            }

            create_event(event)

            project.save()
            '''
            Se busca el proyecto guardado con la finalidad de guardarlo en TeamWork
            '''
            new_project= Project.objects.get(code = project.code)
            '''
            Se cambia el formato de las fechs a como es aceptado en TeamWork
            '''
            startDate = str(new_project.startDate).split('-')
            endDate = str(new_project.endDate).split('-')

            #####################Conexion con Team Work###############################
            id_team_work= add_project(project.name, project.description, ''.join(startDate), ''.join(endDate))
            print(id_team_work)
            project.idTeamWorkProject=id_team_work
            project.save()
            project.save()
            ##################################################

            '''
            Se guarda la relación entre el cliente y el proyecto.
            '''
            project_user_client = ProjectUser(user= profile_client, project=new_project)
            '''
            Se guarda la relación entre el responsable por parte de IDBC y el proyecto.
            '''
            project_user_emp = ProjectUser(user= profile_emp, project=new_project, isResponsable= True)

            project_user_client.save()
            project_user_emp.save()
            messages.success(request, "El projecto ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('new_project'))
        else:
            messages.success(request, "Error al registrar el proyecto")

            return render(request, 'page-new-project.html', {'form': form})

'''
Clase que permite modificar un proyecto.
'''
class Update_Project(TemplateView):
    template_name = 'page-new-project.html'
    form_class = UpdateProjectForm

    def get_context_data(self, **kwargs):
        context = super(
            Update_Project, self).get_context_data(**kwargs)
        context['title'] ='Modificar'
        project = Project.objects.get(code=self.kwargs['pk'])
        '''
        Se verifica si los proyectos tienen fechas asociadas de modo que sean mostradas en la respectiva vista. 
        '''
        if project.startDate == None:
            startDate = ''
        else:
            startDate = project.startDate.strftime("%d-%m-%Y")
        if project.endDate == None:
            endDate = ''
        else:
            endDate = project.endDate.strftime("%d-%m-%Y")

        projectUser = ProjectUser.objects.filter(project_id=project.code)
        client=''
        responsable = ''
        for i in projectUser:
            profileUser = ProfileUser.objects.get(id = i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)

            if i.isResponsable:
                responsable=user
            else:
                if str(user.groups.all()[0])=='Cliente':
                    client=user
        data = {'name':project,
                'client':client,
                'company': responsable,
                'startDate': startDate,
                'endDate': endDate,
                'status': project.status,
                'description':project.description
        }

        form = NewProjectForm(initial=data)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = UpdateProjectForm(post_values)
        if form.is_valid():
            project_pk = kwargs['pk']
            project = Project.objects.get(pk = project_pk)
            '''
            En caso de que sea el mismo proyecto pero diferente responsable, se busca el responsable actual
            '''
            # caso 1: mismo codigo diferente responsable
            old_responsable = ProjectUser.objects.filter(project = project, isResponsable=True).exists()
            project.name=post_values['name']
            project.status = post_values['status']
            auth_cliente = post_values['client']
            auth_emp = post_values['company']
            # id de nuevo responsable de la empresa
            profile_emp = ProfileUser.objects.get(fk_profileUser_user_id = auth_emp)
            userProject = ProjectUser.objects.filter(user_id=profile_emp.pk, project=project)
            if userProject:
                # caso de que exista la relacion entre usuario y proyecto pero no es responsable
                for i in userProject:
                    if i.isResponsable == False:
                        relation = ProjectUser.objects.get(id=i.id)
                        if old_responsable:
                            old_responsable = ProjectUser.objects.get(project = project, isResponsable=True)
                            old_responsable.isResponsable = False
                            old_responsable.save()
                        relation.isResponsable = True
                        relation.save()
                    else:
                        pass

            else:
                if old_responsable:
                    old_responsable = ProjectUser.objects.get(project = project, isResponsable=True)
                    old_responsable.isResponsable = False
                    old_responsable.save()
                project_user_emp = ProjectUser(user= profile_emp, project=project, isResponsable= True)
                project_user_emp.save()

            profile_client = ProfileUser.objects.get(fk_profileUser_user = auth_cliente)
            old_client = ProjectUser.objects.filter(user=profile_client.pk, project=project)
            print("viejo cliente " + str(old_client))
            if not old_client:
                print("no existe")
                newRelationClient = ProjectUser(project_id = project.code, user_id=profile_client.id, isResponsable=False)
                projectUser = ProjectUser.objects.filter(project_id=project.code)
                for i in projectUser:
                    print(i.user_id)
                    profileUser = ProfileUser.objects.get(id = i.user_id)
                    user = User.objects.get(id=profileUser.fk_profileUser_user_id)
                    print(user)
                    if str(user.groups.all()[0]) == "Cliente":
                        deleteClient = ProjectUser.objects.get(user_id=profileUser)
                        print("me van a eliminar " +str(deleteClient.user_id))
                        deleteClient.delete()
                newRelationClient.save()
            a = post_values['startDate'].split('-')
            startDate = a[2]+'-'+a[1]+'-'+a[0]
            print(startDate)
            project.startDate =startDate
            b = post_values['endDate'].split('-')
            endDate = b[2]+'-'+b[1]+'-'+b[0]
            project.endDate = endDate
            project.description = post_values['description']

            project.save()
            project = Project.objects.get(code = project.code)
            print("aquiiiiii antes de la fecha")
            print(str(project.startDate).split('-'))
            startDate = str(project.startDate).split('-')
            endDate = str(project.endDate).split('-')
            print(''.join(startDate))

            # ****************** Team Work ***********************
            print("AQUIIIIIIII")

            print(request.method)
            UpdateProjectTW(project.idTeamWorkProject, project.name, ''.join(startDate), ''.join(endDate),
                            project.description)
            print("Despues del update")

            # *******************************************************

            messages.success(request, "El proyecto ha sido modificado exitosamente")
            return HttpResponseRedirect(reverse_lazy('project'))
        else:
            return render(request, 'page-new-project.html', {'form':form, 'pk':self.kwargs['pk']})

'''
Clase que permite detallar un proyecto.
'''
class Detail_Project(TemplateView):
    template_name = 'page-detail-project.html'
    form_class= statusForm

    def get_context_data(self, **kwargs):
        context = super(
            Detail_Project, self).get_context_data(**kwargs)
        project = Project.objects.get(code=self.kwargs['pk'])
        '''
        Documentos asociados a un proyecto.
        '''
        documents = Documents.objects.filter(fk_documents_project=project)
        users = User.objects.all()

        '''
        Tareas relacionadas a un proyecto.
        '''

        user_pk= self.request.user.id
        user = User.objects.get(pk=user_pk)
        profileUser = ProfileUser.objects.get(fk_profileUser_user_id = user_pk)
        if (user.has_perms(['project.add_project'])):
            task = Task.objects.filter(project=project)
        else:
            task= Task.objects.filter(users=profileUser.pk,project=project)
        dependencys = Dependency.objects.all()

        projectUser = ProjectUser.objects.filter(project_id=project.code)
        now = datetime.datetime.now()
        '''
        En caso de que no se tenga una frecha establecida, se muestra '---'
        '''
        if (project.endDate == None):
            project.endDate = "----"
            context['resta']= project.endDate
        else:
            '''
            Se resta el día de culminación del proyecto con el día actual, para saber cuante tiempo queda para entregar el proyecto.
            '''
            resta = project.endDate - now.date()
            context['resta'] = resta.days

            '''
            Esto se qeuría hacer con la finalidad de enviar un correo de recordatorio, al restar un día, sin embargo 
            debe hacerse en otro lado
            '''
            # if resta.days == 1:
            #     emailUser =[]
            #     for i in projectUser:
            #         emailUser.append(i.user.fk_profileUser_user.email)
            #     print("correoooooosss")
            #     print(emailUser)
            #     email_subject = 'IDBC Group - Entrega de  ' + str(project.name)
            #     message_template = 'emailEndProject.html'
            #     c = {'project': project.name,
            #          'endDate':project.endDate
            #          }
            #
            #
            #     send_email(email_subject, message_template, c, emailUser)
        '''
        En caso de que el proyecto no cuente con una descripción, se mostrará 'Descripción no disponible'
        '''
        if (project.description == ''):
            project.description = 'Descripción no disponible'
        '''
        En caso de que el proyecto no cuente con las fechas establecidas, se mostrará 'No disponible'
        '''
        if project.startDate == None or project.endDate== None:
            project.startDate = 'No Disponible'
            project.endDate = 'No Disponible'

        '''
        Inicialmente, se colocará al cliente 'No disponible'. Si el el proyecto cuenta con un cliente, esta variable 
        cambia con el nombre del mismo
        '''
        client ='No Disponible'
        for i in projectUser:
            profileUser = ProfileUser.objects.get(id = i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            '''
            Si el usuario ocupa el rol de cliente, la variable client tendrá este nombre
            '''
            if str(user.groups.all()[0]) == "Cliente":
                client = user.get_full_name()

        '''
        Se guarda en un arreglo los estados del proyecto. Estos estados pueden verse por el responsable del proyecto.
        '''
        status_project= ['In Progress','Technical Review','Functional Review', 'Customer Acceptance','Done']
        '''
        Estos status se pueden ver por el resto de los usuarios.
        '''
        status = ['In Progress','Technical Review']


        context['tasks'] = task
        context['dep'] = dependencys
        context['project'] = project
        context['client'] = client
        context['projectUser'] = projectUser
        context['status_project'] = status_project
        context['status']=status
        context['documents']=documents
        context['users']=users

        return context

'''
Función que permite crear el código del proyecto.
@:param name: Nombre del proyecto.
@:return las tres primeras letras del proyecto.
'''
def codeProject(name):
    name = ''.join(name)
    return name[:3]

'''
Función que permite validar el nombre de un proyecto.
'''
def ValidateName(request):
    name = request.POST.get('name', None)
    data = {
        'name_exists': Project.objects.filter(name=name).exists()
    }

    return JsonResponse(data)

'''
Función que envía los datos por un formato Json a un JS para construir el diagrama de barras. 
'''
def BarProgress(request):
    user = request.user.id
    user_pk = User.objects.get(pk=user)

    '''
    Si el usuario cuenta con los permisos de agregar un proyecto, se le muestra en el diagrama todos los proyectos
    registrados en el sistema
    '''
    if (user_pk.has_perms(['project.add_project'])):
        proj = Project.objects.all()
        x = [p.name for p in proj]
        '''
        En caso contrario, solo se le muestran los proyectos a los cuales él esté vinculado.
        '''
    else:
        user = ProfileUser.objects.get(fk_profileUser_user=user_pk)
        proj = ProjectUser.objects.filter(user=user)
        x=[]
        for i in proj:
            x.append(Project.objects.get(code=i).name)
    '''
    Estimada se refiere a la cantidad de días que ha de durar un proyecto, esto a través de la duración de sus tareas.
    Real se refiere a la verdadera cantidad de días que se demoró el proyecto, esto en vista a la duración de las tareas.
    '''

    array = ([
        ['Proyecto', 'Estimada', 'Real']
    ])

    duration = []
    durationDone =[]
    for i in x:
        project = Project.objects.get(name=i)
        tasksCount = Task.objects.filter(project_id=project.code).count()
        '''
        En caso de que un proyecto no cuente con tareas asociadas, en el diagrama de barra se mostrará unicamente el 
        nombre del proyecto
        '''
        if tasksCount == 0:
            days = 0
            real=0
            array.append([i,days,real])
        else:
            tasks = Task.objects.filter(project_id=project.code)
            for task in tasks:
                '''
                La duración de los dias estimados se calcula en base a la resta de la fecha final establecida en un 
                principio menos la fecha inicial
                '''
                days = task.endDate - task.startDate
                '''
                Como se necesita tener la cantidad de días que dura cada tarea, se procede a guardar en un arreglo la 
                duración de cad tarea, con la finalidad de sumarlos todos y poder tener un total de días establecidos.
                '''
                duration.append(days.days)
            days=sum(duration)
            duration = []

            '''
            Para calcular la cantidad de tareas que ya han sido terminadas, es decir, que su status se encuentre en
            estado 'Done', se procede a filtrar estas tareas con este status.
            '''
            taskDone = Task.objects.filter(project_id=project.code, status='Done')
            if taskDone:
                for t in taskDone:
                    '''
                    Como al cambiar el estado de una tarea en Done, se almacena la fecha de culminación del mismo, ésta
                    es la mostrada en el diagrama de barras como 'Real'.
                    '''
                    daysDone = t.endDateReal - t.startDate
                    durationDone.append(daysDone.days)
                daysDone = sum(durationDone)
                durationDone = []

                array.append([project.name,days,daysDone])
            else:
                array.append([project.name, days, 0])

    return JsonResponse(array, safe=False)

'''
Función que permite mostrar los detalles de un proyecto, es decir, permite dirigir hacia la vista de 'Detail Project'
Para esto, se envía toda la información necesaria mediante un Json a un JS.
'''
def ShowDetails(request):
    nameProject = request.GET.get('nameProject', None)

    data = {'project': Project.objects.filter(name=nameProject).exists()}

    if data['project']:
        project = Project.objects.get(name=nameProject)
        projectUser = ProjectUser.objects.filter(project_id = project.code)
        data['client'] = 'No disponible'
        data['responsable'] = 'No disponible'
        for i in projectUser:
            profileUser = ProfileUser.objects.get(id=i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            if i.isResponsable:
                data['responsable']=user.get_full_name()
            else:
                if str(user.groups.all()[0]) == "Cliente":
                    data['client'] = user.get_full_name()

        data['name']= project.name
        data['start'] = project.startDate
        if data['start']== None:
            data['start'] = 'No disponible'
        else:
            data['start'] = project.startDate.strftime("%d-%m-%Y")
        data['end'] = project.endDate
        if data['end'] == None:
            data['end'] = 'No disponible'
        else :
            data['end'] = project.endDate.strftime("%d-%m-%Y")
        data['status'] = project.status
        if data['status'] == '':
            data['status'] = "Sin status"
        return JsonResponse(data)

'''
Función que permite obtener el código de un proyecto, con la finalidad de redirigir a la página de 'Detail Project' de
cada uno de los proyectos.
'''
def getCode(request):
    nameProject= request.GET.get('nameProject',None)
    data ={'code' : Project.objects.get(name=nameProject).code}
    return JsonResponse(data)

'''
Función que permite eliminar un proyecto.
@:param code: Código del proyecto.
'''
def DeleteProject(request,code):
    project = Project.objects.get(code=code)
    task = Task.objects.filter(project=project.code).count()
    '''
    Si el proyecto tiene al menos una tarea asociada el proyecto no se puede eliminar.
    '''
    if task > 0:
        messages.success(request, "El proyecto " + str(project.name) + " tiene tareas asociadas. No se puede eliminar")
        return HttpResponseRedirect(reverse_lazy('project'))
    else:
        DeleteProjectTW(project.idTeamWorkProject)
        project.delete()
        messages.success(request, "El proyecto " + str(project.name) + " se ha eliminado exitosamente")
        return HttpResponseRedirect(reverse_lazy('project'))

'''
Clase que permite la visualización de los documentos pertenecientes a un proyecto.
'''
class DocumentsView(FormView):
    template_name = 'page-detail-project.html'
    form_class = DocumentsForm

    def post(self, request, *args, **kwargs):
        form = DocumentsForm(request.POST, request.FILES)
        if form.is_valid():
            project_pk = self.kwargs['pk']
            project = Project.objects.get(pk=project_pk)
            if (request.FILES == {}):
                pass
            else:
                '''
                Como al agregar un documento, se pueden agregar varios simultaneamente, se obtienen todos los documentos
                con sus descripciones ingresados por el usuario. Luego se almacenan en su respecctiva tabla.
                '''
                desc = request.POST.getlist('description')
                files =request.FILES.getlist('file')
                for i in zip(files, desc):
                    doc = Documents(file=i[0],
                                    fk_documents_project= project,
                                    description=i[1])
                    doc.save()
                    '''
                    Luego de guardarlo en la base de datos, se procede a almacenar el documento en el google Drive del
                    correo asociado. 'path' se refiere a la ruta donde serán almacenados los docuemntos 
                    '''
                    path= 'ProjectManagement/static/media/'+str(doc.file)
                    upload_file(path)

            messages.success(request, "El Documento ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('detail_project',kwargs={"pk":self.kwargs['pk']}))
        else:
            messages.success(request, "No se puede guardar el documento")
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))

'''
Clase que permite agregar más usuarios a un proyecto. Estos usuarios deberán estar registrados previamente en el
sistema
'''
class MoreUsersView(FormView):
    template_name = 'page-detail-project.html'
    form_class = MoreUsersForm

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = MoreUsersForm(post_values)
        if form.is_valid():
            project_pk = self.kwargs['pk']
            project = Project.objects.get(code=project_pk)

            '''
            Se obtiene la lista de todos los usuarios ingresados por el usuario.
            '''
            users = post_values.getlist('user')
            for user in users:
                user = User.objects.get(pk=user)
                userProfile = ProfileUser.objects.get(fk_profileUser_user=user)
                existUser = ProjectUser.objects.filter(user=userProfile, project=project).exists()

                if not existUser:
                    projectUser = ProjectUser(isResponsable=False, project=project, user=userProfile)
                    projectUser.save()
            messages.success(request, "La/as persona/as se ha agregado al proyecto "+str(project.name))
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))
        else:
            project = Project.objects.get(code=self.kwargs['pk'])
            messages.success(request, "Erro al registrar usuarios en el proyecto " + str(project.name))
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))

'''
Función que permite mostrar la tabla de tareas asociadas a un proyecto. La información es enviada mediante Json
a un JS.
'''
def ShowTable(request):
    nameProject = request.GET.get('nameProject', None)
    project=Project.objects.get(name=nameProject)
    data = {'project': Project.objects.filter(name=nameProject).exists()}
    # Usuario que inicia sesion
    user = request.user.id
    user_pk = User.objects.get(pk=user)
    profileUser = ProfileUser.objects.get(fk_profileUser_user=user_pk)

    '''
    Si el usuario tiene permisos de agregar un proyecto se muestran todos las tareas asociadas al proyecto
    '''

    if (user_pk.has_perms(['project.add_project'])):
        task = Task.objects.filter(project=project)
    else:
        '''
        De lo contrario, solo se muestran las tareas correspondientes al usuario 
        '''
        task = Task.objects.filter(users=profileUser.pk, project=project)

    x = []
    j = 0
    for i in task:
        # usuario dueño de la tarea
        user=User.objects.get(pk=i.users.fk_profileUser_user_id)
        dependence = Dependency.objects.filter(task_id=i.code)
        d = [] # Arreglo de las tareas que dependen 'requieren de'.
        for dep in dependence:
            d.append(dep.dependence)
        d = (' ').join(d)
        required= Dependency.objects.filter(dependence=i.code)
        r = [] # Arreglos de las tareas que requieren de una tarea 'requerido por'
        for req in required:
            r.append(req.task_id)
        r = (' ').join(r)
        a = i.startDate
        start = str(a.day)+'-'+str(a.month)+'-'+str(a.year)
        b = i.endDate
        end = str(b.day)+'-'+str(b.month)+'-'+str(b.year)
        '''
        La información es enviada mediante arrelgos de arrelgos.
        '''
        y=[]
        y.append(i.code)
        y.append(i.name)
        y.append(user.first_name)
        y.append(user.last_name)
        y.append(start)
        y.append(end)
        y.append(r)
        y.append(d)
        y.append(i.status)
        x.append(y)
        j =j+1

    data['task']=x

    return JsonResponse(data)

'''
Clase que permite el cambio de status de una tarea
'''
class ChangeStatus(TemplateView):
    template_name = 'page-detail-project.html'
    form_class= statusForm

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = statusForm(post_values)
        if form.is_valid():
            project_pk = self.kwargs['pk']
            code_task = self.kwargs['code']
            user_pk = self.request.user.id
            users = User.objects.get(pk=user_pk)
            project = Project.objects.get(pk=project_pk)
            task = Task.objects.get(code=code_task, project=project_pk)
            #Se calcula la fecha actual para saber cuando se cambia el status
            endDateReal = datetime.date.today()
            task.endDateReal = endDateReal
            # Si la fecha de inicio de la tarea es mayor que la actual no se debe cambiar el status
            if (task.startDate > task.endDateReal ):
                messages.success(request, "La tarea "+str(task.name)+ " no ha sido iniciada. No puede cambiar su status")
                return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))
            old_status = task.status
            task.status = post_values['status']
            projectUser = ProjectUser.objects.filter(project_id = project)

            '''
            Se envía un correo electrónico informando a los usuarios interesados que se ha cambiado el status de una 
            determinada tarea. Estos usuarios interesados son el responsable de la tarea y el responsable de IDBC del proyecto
            '''
            email_subject = 'IDBC Group - Cambio de Estado de tarea del proyecto ' + str(project.name)
            message_template = 'emailStatusTask.html'
            for i in projectUser:
                if i.isResponsable == True:
                    name_responsable = i.user.fk_profileUser_user.first_name
                    email_responsable = [i.user.fk_profileUser_user.email]
                    c = {'usuario': name_responsable,
                         'name_task': task.name,
                         'project' : project.name,
                         'user':users.first_name +' '+users.last_name,
                         'old_status':old_status,
                         'new_status': task.status,
                         'host': request.META['HTTP_HOST']
                         }
                    send_email(email_subject, message_template, c, email_responsable)

            email_task = [task.users.fk_profileUser_user.email]
            name_responsable = task.users.fk_profileUser_user.first_name
            c = {'usuario': name_responsable,
                 'name_task': task.name,
                 'project': project.name,
                 'user': users.first_name + ' ' + users.last_name,
                 'old_status': old_status,
                 'new_status': task.status,
                 'host': request.META['HTTP_HOST']
                 }
            send_email(email_subject, message_template, c, email_task)
            task.save()
            messages.success(request, "El status de la tarea ha sido modificado exitosamente")
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))
        else:
            messages.success(request, "Error al cambiar status de tarea")
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))

'''
Función que permite activar el botón de cerrar proyecto, siempre y cuando todas sus tareas asociadas estén en estado
'Done' 
'''
def ChangeButton(request):
    code = request.GET.get('code', None)
    all_task = Task.objects.filter(project=code).count()
    done_task = Task.objects.filter(project=code, status="Done").count()

    data = {
        'name_exists': Project.objects.filter(code=code).exists()
    }
    project = Project.objects.get(code=code)
    data['code'] = code
    data['all_task']= all_task
    data['done_task']=done_task
    data['status']=project.status

    return JsonResponse(data)

'''
Función que permite cerrar un proyecto siempre y cuando el status del mismo sea 'Done'
@:param pk: identificador del proyecto.
'''
def CloseProject(request, pk):
    project = Project.objects.get(code=pk)
    project.status ='Done'
    project.save()
    messages.success(request, "El Proyecto "+str(project.name)+ " se ha cerrado.")
    return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": project.code}))




















