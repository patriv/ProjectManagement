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
            project.code = codeProject(project.name)
            project.start_date = post_values['start_date']
            project.end_date = post_values['end_date']
            project.status = post_values['status']
            project.description = post_values['description']
            print(project.start_date)
            project.save()
            messages.success(request, "El projecto ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('new_project'))
        else:
            form.add_error(None, "Error al registrar el proyecto")
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



