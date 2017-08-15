# -*- coding: utf-8 -*-
import hashlib
import random
import json
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import *
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.forms import *
from project.models import *
from task.models import *
from django.urls import reverse

from users.views import send_email

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(
            Home, self).get_context_data(**kwargs)
        print("get")
        project = Project.objects.all()
        print(project)
        context['project'] = project
        print(context)
        return context

class New_Project(FormView):
    template_name = 'page-new-project.html'
    form_class = NewProjectForm

    def get_context_data(self, **kwargs):
        context = super(
            New_Project, self).get_context_data(**kwargs)
        print("get")
        context['title'] = 'Agregar'
        return context

    def post(self, request, *args, **kwargs):
        print("en post project")
        post_values = request.POST.copy()
        form = NewProjectForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            project = form.save(commit=False)
            project.name = post_values['name']
            print(project.name)
            code = codeProject(project.name)
            print("esto es code")
            print(code)
            code_exist = Project.objects.filter(code=code).exists()
            print(code_exist)
            if code_exist:
                length = len(code)
                code = code + project.name[length]
                print("new code")
                print(code)
                project.code=code
            else:
                project.code = code
            a = post_values['startDate'].split('-')
            startDate = a[2]+'-'+a[1]+'-'+a[0]
            project.startDate = startDate
            b = post_values['endDate'].split('-')
            endDate = b[2] + '-' + b[1] + '-' + b[0]
            project.endDate = endDate
            project.status = post_values['status']
            project.description = post_values['description']
            print(project.startDate)
            auth_cliente = post_values['client']
            auth_emp = post_values['company']
            print("comany")
            print(auth_emp)
            # id de responsable de la empresa
            profile_emp = ProfileUser.objects.get(fk_profileUser_user_id = auth_emp)
            print(profile_emp.pk)
            # id del cliente
            profile_client = ProfileUser.objects.get(fk_profileUser_user = auth_cliente)
            print(profile_client.id)
            project.save()
            new_project= Project.objects.get(code = project.code)
            print(new_project)
            # relacion cliente proyecto
            project_user_client = ProjectUser(user= profile_client, project=new_project)
            #relacion empresa proyecto
            project_user_emp = ProjectUser(user= profile_emp, project=new_project, isResponsable= True)
            project_user_client.save()
            project_user_emp.save()
            messages.success(request, "El projecto ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('new_project'))
        else:
            messages.success(request, "Error al registrar el proyecto")
            return HttpResponseRedirect(reverse_lazy('new_project'))

class Update_Project(TemplateView):
    template_name = 'page-new-project.html'
    form_class = UpdateProjectForm

    def get_context_data(self, **kwargs):
        context = super(
            Update_Project, self).get_context_data(**kwargs)
        print("get de update project")
        context['title'] ='Modificar'
        project = Project.objects.get(code=self.kwargs['pk'])
        print(project.startDate)
        if project.startDate == None:
            startDate = ''
        else:
            startDate = project.startDate.strftime("%d-%m-%Y")
        if project.endDate == None:
            endDate = ''
        else:
            endDate = project.endDate.strftime("%d-%m-%Y")

        projectUser = ProjectUser.objects.filter(project_id=project.code)
        print("soy project user")
        print(projectUser)
        client=''
        responsable = ''
        for i in projectUser:
            print("dentro de for")
            print(i.user_id)
            profileUser = ProfileUser.objects.get(id = i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            print(user)

            if i.isResponsable:
                print("Soy responsable" + str(i.isResponsable))
                responsable=user
            else:
                print("no es responsable")
                if str(user.groups.all()[0])=='Cliente':
                    client=user



            print(client)


        data = {'name':project,
                'client':client,
                'company': responsable,
                'startDate': startDate,
                'endDate': endDate,
                'status': project.status,
                'description':project.description
        }
        print(data)

        form = NewProjectForm(initial=data)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        print("post de update project")
        post_values = request.POST.copy()
        form = UpdateProjectForm(post_values)
        if form.is_valid():
            project_pk = kwargs['pk']
            project = Project.objects.get(pk = project_pk)
            print(project.code)
            # caso 1: mismo codigo diferente responsable
            old_responsable = ProjectUser.objects.filter(project = project, isResponsable=True).exists()
            print(old_responsable)

            project.name=post_values['name']
            project.status = post_values['status']

            print("este es el nuevo project" + str(project))

            auth_cliente = post_values['client']
            auth_emp = post_values['company']
            print("comany")
            print(auth_emp)
            print("client" + str(auth_cliente))
            # id de responsable de la empresa
            profile_emp = ProfileUser.objects.get(fk_profileUser_user_id = auth_emp)
            print(profile_emp.pk)
            userProject = ProjectUser.objects.filter(user_id=profile_emp.pk, project=project)
            print(userProject)
            if userProject:
                # caso de que exista la relacion entre usuario y proyecto pero no es responsable
                for i in userProject:
                    if i.isResponsable == False:
                        print("is false")
                        print(i.id)
                        relation = ProjectUser.objects.get(id=i.id)
                        print(relation)
                        if old_responsable:
                            old_responsable = ProjectUser.objects.get(project = project, isResponsable=True)
                            old_responsable.isResponsable = False
                            old_responsable.save()
                        relation.isResponsable = True
                        relation.save()
                    else:
                        print("sigue siendo el mismo cliente")
                        pass

            else:
                if old_responsable:
                    old_responsable = ProjectUser.objects.get(project = project, isResponsable=True)
                    old_responsable.isResponsable = False
                    old_responsable.save()
                project_user_emp = ProjectUser(user= profile_emp, project=project, isResponsable= True)
                print(project_user_emp)
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
                    group = user.groups.all()[0]
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

            messages.success(request, "El proyecto ha sido modificado exitosamente")
            return HttpResponseRedirect(reverse_lazy('project'))
        else:
            return render(request, 'page-new-project.html', {'form':form, 'pk':self.kwargs['pk']})

class Detail_Project(TemplateView):
    template_name = 'page-detail-project.html'
    form_class= statusForm

    def get_context_data(self, **kwargs):
        context = super(
            Detail_Project, self).get_context_data(**kwargs)
        project = Project.objects.get(code=self.kwargs['pk'])
        # DOCUMENTOS
        documents = Documents.objects.filter(fk_documents_project=project)
        print("**** USUARIOS************")
        users = User.objects.all()

        print("****************TAREAS*****************************")
        # TAREAS

        user_pk= self.request.user.id
        user = User.objects.get(pk=user_pk)
        profileUser = ProfileUser.objects.get(fk_profileUser_user_id = user_pk)
        print(profileUser.pk)
        print(user_pk)
        if (user.has_perms(['project.add_project'])):
            task = Task.objects.filter(project=project)
        else:
            task= Task.objects.filter(users=profileUser.pk,project=project)
        dependencys = Dependency.objects.all()

        now = datetime.datetime.now()
        print(project.endDate)
        if (project.endDate == None):
            project.endDate = "----"
            context['resta']= project.endDate
        else:
            resta = project.endDate - now.date()
            context['resta'] = resta.days

        if (project.description == ''):
            project.description = 'Descripción no disponible'

        if project.startDate == None or project.endDate== None:
            project.startDate = 'No Disponible'
            project.endDate = 'No Disponible'
        projectUser = ProjectUser.objects.filter(project_id=project.code)
        client ='No Disponible'
        for i in projectUser:
            print(i.user_id)
            profileUser = ProfileUser.objects.get(id = i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            print(user)

            group = user.groups.all()[0]
            if str(user.groups.all()[0]) == "Cliente":
                client = user.get_full_name()

        status_project= ['In Progress','Technical Review','Functional Review', 'Customer Acceptance','Done']
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

def codeProject(name):
    name = ''.join(name)
    return name[:3]

def ValidateName(request):
    name = request.POST.get('name', None)
    data = {
        'name_exists': Project.objects.filter(name=name).exists()
    }

    return JsonResponse(data)

def BarProgress(request):
    user = request.user.id
    user_pk = User.objects.get(pk=user)

    print(user_pk.has_perms(['project.add_project']))
    if (user_pk.has_perms(['project.add_project'])):
        proj = Project.objects.all()
        x = [p.name for p in proj]
    else:
        user = ProfileUser.objects.get(fk_profileUser_user=user_pk)
        proj = ProjectUser.objects.filter(user=user)
        x=[]
        for i in proj:
            x.append(Project.objects.get(code=i).name)

    print(proj)
    array = ([
        ['Proyecto', 'Estimada', 'Real']
    ])

    print(x)
    duration = []
    durationDone =[]
    for i in x:
        project = Project.objects.get(name=i)
        print("******* PROJECT *******************")
        print(project)
        tasksCount = Task.objects.filter(project_id=project.code).count()
        if tasksCount == 0:
            days = 0
            array.append([i,days,0])
        else:
            tasks = Task.objects.filter(project_id=project.code)
            print("soy tareas" + str(tasks))
            for task in tasks:
                print(task)
                days = task.endDate - task.startDate
                print("soy los dias "+str(days.days))
                print(duration)
                duration.append(days.days)
            days=sum(duration)
            duration = []
            print(duration)

            taskDone = Task.objects.filter(project_id=project.code, status='Done')
            print("")
            print(taskDone)
            if taskDone:
                for t in taskDone:
                    print(t.startDate)
                    print(t.endDateReal)
                    daysDone = t.endDateReal - t.startDate
                    print(daysDone.days)
                    durationDone.append(daysDone.days)
                print(durationDone)
                daysDone = sum(durationDone)
                durationDone = []

                array.append([project.name,days,daysDone])
            else:
                array.append([project.name, days, 0])


    print(array)

    return JsonResponse(array, safe=False)

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
                group = user.groups.all()[0]
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

def getCode(request):
    nameProject= request.GET.get('nameProject',None)
    data ={'code' : Project.objects.get(name=nameProject).code}
    return JsonResponse(data)

class DocumentsView(FormView):
    template_name = 'page-detail-project.html'
    form_class = DocumentsForm

    def post(self, request, *args, **kwargs):
        print("en post Documets")
        form = DocumentsForm(request.POST, request.FILES)
        print(form.is_valid())
        print(form)
        if form.is_valid():
            project_pk = self.kwargs['pk']
            project = Project.objects.get(pk=project_pk)

            print(project)
            if (request.FILES == {}):
                pass
            else:
                desc = request.POST.getlist('description')
                files =request.FILES.getlist('file')
                for i in zip(files, desc):
                    doc = Documents(file=i[0],
                                    fk_documents_project= project,
                                    description=i[1])
                    doc.save()

            messages.success(request, "El Documento ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('detail_project',kwargs={"pk":self.kwargs['pk']}))
        else:
            messages.success(request, "No se puede guardar el documento")
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))

class MoreUsersView(FormView):
    template_name = 'page-detail-project.html'
    form_class = MoreUsersForm

    def post(self, request, *args, **kwargs):
        print("more users")
        post_values = request.POST.copy()
        form = MoreUsersForm(post_values)
        print(form)
        if form.is_valid():
            project_pk = self.kwargs['pk']
            project = Project.objects.get(code=project_pk)

            users = post_values.getlist('user')
            for user in users:
                user = User.objects.get(pk=user)
                userProfile = ProfileUser.objects.get(fk_profileUser_user=user)
                existUser = ProjectUser.objects.filter(user=userProfile, project=project).exists()
                print("existe " + str(existUser))
                print(user)
                if not existUser:
                    projectUser = ProjectUser(isResponsable=False, project=project, user=userProfile)
                    projectUser.save()
            messages.success(request, "La/as persona/as se ha agregado al proyecto "+str(project.name))
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))
        else:
            project = Project.objects.get(code=self.kwargs['pk'])
            messages.success(request, "Erro al registrar usuarios en el proyecto " + str(project.name))
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))

def ShowTable(request):
    nameProject = request.GET.get('nameProject', None)
    print("*********** EN AJAX ********************")
    print(nameProject)
    project=Project.objects.get(name=nameProject)
    data = {'project': Project.objects.filter(name=nameProject).exists()}
    # Usuario que inicia sesion
    user = request.user.id
    user_pk = User.objects.get(pk=user)
    profileUser = ProfileUser.objects.get(fk_profileUser_user=user_pk)
    if (user_pk.has_perms(['project.add_project'])):
        task = Task.objects.filter(project=project)
    else:
        task = Task.objects.filter(users=profileUser.pk, project=project)

    x = []
    j = 0
    for i in task:
        print(i.name)
        # usuario dueño de la tarea
        user=User.objects.get(pk=i.users.fk_profileUser_user_id)
        dependence = Dependency.objects.filter(task_id=i.code)
        d = []
        for dep in dependence:
            print()
            d.append(dep.dependence)
        d = (' ').join(d)
        required= Dependency.objects.filter(dependence=i.code)
        r = []
        for req in required:
            r.append(req.task_id)
        r = (' ').join(r)
        a = i.startDate
        start = str(a.day)+'-'+str(a.month)+'-'+str(a.year)
        b = i.endDate
        end = str(b.day)+'-'+str(b.month)+'-'+str(b.year)
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
    print(x)
    data['task']=x

    return JsonResponse(data)

class ChangeStatus(TemplateView):
    template_name = 'page-detail-project.html'
    form_class= statusForm

    def post(self, request, *args, **kwargs):
        print("post de STATUUUUUUSSSS")
        post_values = request.POST.copy()
        form = statusForm(post_values)
        print(form)
        if form.is_valid():
            project_pk = self.kwargs['pk']
            code_task = self.kwargs['code']
            print(project_pk)
            print(code_task)
            user_pk = self.request.user.id
            users = User.objects.get(pk=user_pk)
            project = Project.objects.get(pk=project_pk)
            print(project.code)
            task = Task.objects.get(code=code_task, project=project_pk)
            print("status viejo")
            print(task.status)
            old_status = task.status
            task.status = post_values['status']
            print("task.status nuevo " + str(task.status))
            #task = Task.objects.get(code = code_task)
            print(task.users.fk_profileUser_user.email)
            projectUser = ProjectUser.objects.filter(project_id = project)
            print(projectUser)
            email_subject = 'IDBC Group - Cambio de Estado de tarea del proyecto ' + str(project.name)
            message_template = 'emailStatusTask.html'
            for i in projectUser:
                if i.isResponsable == True:
                    name_responsable = i.user.fk_profileUser_user.first_name
                    email_responsable = i.user.fk_profileUser_user.email
                    print(email_responsable)
                    print(i.user_id)
                    c = {'usuario': name_responsable,
                         'name_task': task.name,
                         'project' : project.name,
                         'user':users.first_name +' '+users.last_name,
                         'old_status':old_status,
                         'new_status': task.status,
                         'host': request.META['HTTP_HOST']
                         }
                    print(c)
                    print(email_responsable)

                    send_email(email_subject, message_template, c, email_responsable)

            email_task = task.users.fk_profileUser_user.email
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

            endDateReal = datetime.date.today()
            print(endDateReal)
            task.endDateReal = endDateReal
            task.save()
            print("despues de save")

            messages.success(request, "El status de la tarea ha sido modificado exitosamente")
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))
        else:
            messages.success(request, "Error al cambiar status de tarea")
            return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": self.kwargs['pk']}))

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

def CloseProject(request, pk):
    print("Close Project")
    project = Project.objects.get(code=pk)
    print(project.status)
    project.status ='Done'
    print(project.status)
    project.save()


    messages.success(request, "El Proyecto "+str(project.name)+ " se ha cerrado.")
    return HttpResponseRedirect(reverse_lazy('detail_project', kwargs={"pk": project.code}))




















