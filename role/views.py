# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.forms import *
from role.forms import RoleForm

# Ver role

class Role(TemplateView):
    template_name = 'page-role.html'

    def get_context_data(self, **kwargs):
        context = super(
            Role, self).get_context_data(**kwargs)
        role=Group.objects.all()
        context['roles'] = role
        return context


class AddRole(FormView):
    template_name= 'page-role.html'
    form_class = RoleForm   

    def get_context_data(self, **kwargs):
        context = super(
        AddRole, self).get_context_data(**kwargs)
        context['title'] = 'Agregar'
        return context    

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = RoleForm(post_values)
        if form.is_valid():
            newRole = form.save()
            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            messages.error(request, "Introduzca un rol válido")
            return HttpResponseRedirect(reverse_lazy('role'))


def DeleteRole(request,id):
    role = Group.objects.get(pk=id)
    role.delete()
    messages.success(request, "El rol " + str(role.name) +" se ha eliminado exitosamente")
    return HttpResponseRedirect(reverse_lazy('role'))


class UpdateRole(FormView):
    template_name = 'page-role.html'
    form_class = RoleForm

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = RoleForm(post_values)

        if form.is_valid():
            pk = kwargs['id']
            role = Group.objects.get(id = pk)
            role.name = request.POST['name']
            role.save()
            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            messages.error(request, "Introduzca un rol válido")
            return HttpResponseRedirect(reverse_lazy('role'))





