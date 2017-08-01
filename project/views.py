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

        for i in projectUser:
            print("dentro de for")
            print(i.user_id)
            profileUser = ProfileUser.objects.get(id = i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            print(user)

            if i.isResponsable:
                print("Soy responsable" + str(i.isResponsable))
                responsable=user.username
            else:
                print("no es responsable")
                group = user.groups.all()[0]
                countGroup = user.groups.filter(name='Cliente').count()
                print("cuenta de grupo "+str(countGroup))
                if countGroup == 0:
                    client=''
                else:
                    client = user.username

            countProject = ProjectUser.objects.filter(project_id=project.code, isResponsable=True).count()
            if countProject == 0:
                responsable = ''

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

    def get_context_data(self, **kwargs):
        context = super(
            Detail_Project, self).get_context_data(**kwargs)
        project = Project.objects.get(code=self.kwargs['pk'])

        now = datetime.datetime.now()
        resta = project.endDate - now.date()

        if project.startDate == None or project.endDate== None:
            project.startDate = 'No Disponible'
            project.endDate = 'No Disponible'
        projectUser = ProjectUser.objects.filter(project_id=project.code)
        for i in projectUser:
            print(i.user_id)
            profileUser = ProfileUser.objects.get(id = i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            print(user)

            group = user.groups.all()[0]
            if str(user.groups.all()[0]) == "Cliente":
                client = user.get_full_name()


        context['project'] = project
        context['client'] = client
        context['projectUser'] = projectUser
        context['resta'] = resta.days
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
    proj = Project.objects.all()
    print(proj)
    array = ([
        ['Proyecto', 'Estimada', 'Real']
    ])

    x =[p.name for p in proj]
    duration = []
    for i in x:
        project = Project.objects.get(name=i)
        print(project)
        tasksCount = Task.objects.filter(project_id=project.code).count()
        if tasksCount == 0:
            days = 0
            array.append([i,days,100])
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
            array.append([project.name,days,100])
            duration = []

            print(duration)

    print(array)

    return JsonResponse(array, safe=False)

def ShowDetails(request):
    nameProject = request.GET.get('nameProject', None)
    print(nameProject)

    data = {'project': Project.objects.filter(name=nameProject).exists()}

    if data['project']:
        project = Project.objects.get(name=nameProject)
        print("Este es project " + str(project.code))
        projectUser = ProjectUser.objects.filter(project_id = project.code)
        print("projectUser " + str(projectUser))
        data['client'] = 'No disponible'
        data['responsable'] = 'No disponible'
        for i in projectUser:
            profileUser = ProfileUser.objects.get(id=i.user_id)
            user = User.objects.get(id=profileUser.fk_profileUser_user_id)
            if i.isResponsable:
                print("Soy responsable" + str(i.isResponsable))
                data['responsable']=user.get_full_name()
                print('soy responsableee' + str(data['responsable']))

            else:
                print("en else")
                group = user.groups.all()[0]
                print(group)
                print( str(group) == 'Cliente')
                if str(user.groups.all()[0]) == "Cliente":
                    print("si, soy un cliente")
                    data['client'] = user.get_full_name()


        data['name']= project.name
        print(data['name'])
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
        print(JsonResponse(data))
        return JsonResponse(data)

def getCode(request):
    nameProject= request.GET.get('nameProject',None)
    data ={'code' : Project.objects.get(name=nameProject).code}
    return JsonResponse(data)



