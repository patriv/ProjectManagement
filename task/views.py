# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *
from task.forms import *

# Create your views here.


class New_Task(FormView):
    template_name = 'new_work.html'
    form_class = NewTaskForm

    def get_context_data(self, **kwargs):
        context = super(
            New_Task, self).get_context_data(**kwargs)
        print("get")

        context['title'] = 'Agregar'
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
        	return HttpResponseRedirect(reverse_lazy('new_project'))
        else:
            messages.success(request, "Error al registrar el proyecto")
            return HttpResponseRedirect(reverse_lazy('new_project'))

def getCode(request):
	print("getCode")
	nameProject= request.GET.get('nameProject',None)
	data ={'code' : Project.objects.get(name=nameProject).code}
	return JsonResponse(data)



