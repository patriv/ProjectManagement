# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, JsonResponse
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
        print(form)
        if form.is_valid():
            newRole = form.save()
            name = post_values['name']
            print(name)
            group = Group.objects.get(name = name)
            print(group.id)
            project = request.POST.getlist('project')
            print("soy project "+str(project))
            users = request.POST.getlist('users')
            print("soy users " + str(users))
            rol = request.POST.getlist('rol')
            print("soy rol " + str(rol))
            view = request.POST.getlist('view')
            print("soy view " + str(view))
            create = request.POST.getlist('create')
            print("soy create " + str(create))
            update = request.POST.getlist('update')
            print("soy updtae " + str(update))
            delete = request.POST.getlist('delete')
            print("soy delte " + str(delete))
            if project != [] and view != []:
                print("project and view")
                if not (Permission.objects.filter(codename='view_project').exists()):
                    print("no existe ese permiso")
                    content_type = ContentType.objects.get(app_label='project', model='project')
                    permission = Permission.objects.create(codename='view_project',
                                                           name='Can view Project',
                                                           content_type=content_type)
                can_view_project = Permission.objects.get(codename='view_project')
                group.permissions.add(can_view_project.id)


            if rol != [] and create !=[]:
                print("proyecto1")
                can_add_rol = Permission.objects.get(codename = 'add_group')
                print(can_add_rol.id)
                group.permissions.add(can_add_rol.id)
                print("es vacio")
            if rol != [] and update != []:
                print("proyecto2")
                can_update_rol = Permission.objects.get(codename='change_group')
                print(can_update_rol.id)
                group.permissions.add(can_update_rol.id)
                print("es vacio")
            if rol != [] and delete != []:
                print("proyecto3")
                can_delete_rol = Permission.objects.get(codename='delete_group')
                print(can_delete_rol.id)
                group.permissions.add(can_delete_rol.id)
                print("es vacio")


            if project != [] and create !=[]:
                print("proyecto1")
                can_add_project = Permission.objects.get(codename = 'add_project')
                print(can_add_project.id)
                group.permissions.add(can_add_project.id)
                print("es vacio")
            if project != [] and update != []:
                print("proyecto2")
                can_update_project = Permission.objects.get(codename='change_project')
                print(can_update_project.id)
                group.permissions.add(can_update_project.id)
                print("es vacio")
            if project != [] and delete != []:
                print("proyecto3")
                can_delet_project = Permission.objects.get(codename='delete_project')
                print(can_delet_project.id)
                group.permissions.add(can_delet_project.id)
                print("es vacio")

            if users != [] and view != []:
                print("project and view")
                if not (Permission.objects.filter(codename='view_users').exists()):
                    print("no existe ese permiso")
                    content_type = ContentType.objects.get(app_label='auth', model='user')
                    permission = Permission.objects.create(codename='view_users',
                                                           name='Can View Users',
                                                           content_type=content_type)
                can_view_users = Permission.objects.get(codename='view_users')
                group.permissions.add(can_view_users.id)


            if users != [] and create !=[]:
                print("usuario1")
                can_add_users = Permission.objects.get(codename = 'add_user')
                print(can_add_users.id)
                group.permissions.add(can_add_users.id)
                print("es vacio")
            if users != [] and update != []:
                print("usuario2")
                can_update_users = Permission.objects.get(codename='change_user')
                print(can_update_users.id)
                group.permissions.add(can_update_users.id)
                print("es vacio")
            if users != [] and delete != []:
                print("usuario3")
                can_delet_users = Permission.objects.get(codename='delete_user')
                print(can_delet_users.id)
                group.permissions.add(can_delet_users.id)
                print("es vacio")


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

def ViewRole(request):
    name = request.GET.get('name', None)
    print(name)
    role = Group.objects.get(name = name)
   # print(role.)
    data = {
        'role': Group.objects.filter(name=name).exists()
    }
    return JsonResponse(data)







