# -*- coding: utf-8 -*-
import hashlib
import random

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
from django.urls import reverse

class Home(TemplateView):
    template_name = 'index.html'

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
            project.startDate = post_values['startDate']
            project.endDate = post_values['endDate']
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
    template_name = 'page-update-project.html'

class Detail_Project(TemplateView):
    template_name = 'page-detail-project.html'

class New_Task(TemplateView):
    template_name = 'new_work.html'


def codeProject(name):
    name = ''.join(name)
    return name[:3]



