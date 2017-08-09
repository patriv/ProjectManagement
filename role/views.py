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
            newRole.name = post_values['name']
            newRole.save()
            group = Group.objects.get(name = newRole.name)
            print(group.id)
            #Project
            create_project = request.POST.getlist('create_project')
            update_project = request.POST.getlist('update_project')
            view_project = request.POST.getlist('view_project')
            delete_project = request.POST.getlist('delete_project')
            #Users
            create_users = request.POST.getlist('create_users')
            update_users = request.POST.getlist('update_users')
            view_users = request.POST.getlist('view_users')
            delete_users = request.POST.getlist('delete_users')
            print("soy users " + str(create_users))
            #Rol
            create_rol = request.POST.getlist('create_rol')
            update_rol = request.POST.getlist('update_rol')
            view_rol = request.POST.getlist('view_rol')
            delete_rol = request.POST.getlist('view_rol')
            print("soy rol " + str(create_rol))

            #Project
            if  (view_project != []):
                print("project and view")
                if not (Permission.objects.filter(codename='view_project').exists()):
                    print("no existe ese permiso")
                    content_type = ContentType.objects.get(app_label='project', model='project')
                    permission = Permission.objects.create(codename='view_project',
                                                           name='Can view Project',
                                                           content_type=content_type)
                can_view_project = Permission.objects.get(codename='view_project')
                group.permissions.add(can_view_project.id)
            if (create_project != []):
                can_create_project = Permission.objects.get(codename="add_project")
                group.permissions.add(can_create_project)
            if (update_project != []):
                can_change_project = Permission.objects.get(codename="change_project")
                group.permissions.add(can_change_project)
            if (delete_project != []):
                can_delete_project = Permission.objects.get(codename="delete_project")
                group.permissions.add(can_delete_project)

            #ROL
            if (view_rol != []):
                print("project and view")
                if not (Permission.objects.filter(codename='view_group').exists()):
                    print("no existe ese permiso")
                    content_type = ContentType.objects.get(app_label='auth', model='group')
                    permission = Permission.objects.create(codename='view_group',
                                                           name='Can view group',
                                                           content_type=content_type)
                can_view_group = Permission.objects.get(codename='view_group')
                group.permissions.add(can_view_group.id)

            if (create_rol !=[]):
                print("proyecto1")
                can_add_rol = Permission.objects.get(codename = 'add_group')
                print(can_add_rol.id)
                group.permissions.add(can_add_rol.id)
                print("es vacio")
            if (update_rol != []):
                print("proyecto2")
                can_update_rol = Permission.objects.get(codename='change_group')
                print(can_update_rol.id)
                group.permissions.add(can_update_rol.id)
                print("es vacio")
            if  (delete_rol != []):
                print("proyecto3")
                can_delete_rol = Permission.objects.get(codename='delete_group')
                print(can_delete_rol.id)
                group.permissions.add(can_delete_rol.id)
                print("es vacio")

            #Users

            if (view_users != []):
                print("project and view")
                if not (Permission.objects.filter(codename='view_users').exists()):
                    print("no existe ese permiso")
                    content_type = ContentType.objects.get(app_label='auth', model='user')
                    permission = Permission.objects.create(codename='view_users',
                                                           name='Can View Users',
                                                           content_type=content_type)
                can_view_users = Permission.objects.get(codename='view_users')
                group.permissions.add(can_view_users.id)
            if (create_users !=[]):
                print("usuario1")
                can_add_users = Permission.objects.get(codename = 'add_user')
                print(can_add_users.id)
                group.permissions.add(can_add_users.id)
                print("es vacio")
            if (update_users != []):
                print("usuario2")
                can_update_users = Permission.objects.get(codename='change_user')
                print(can_update_users.id)
                group.permissions.add(can_update_users.id)
                print("es vacio")
            if (delete_users != []):
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
    user = role.user_set.exists()
    if user:
        messages.success(request, "El rol "+str(role.name)+ " no se puede eliminar, tiene usuarios asociados.")
        return  HttpResponseRedirect(reverse_lazy('role'))

    else:
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
            group = Group.objects.get(id = pk)
            group.name = request.POST['name']
            group.save()

            # Project
            create_project = request.POST.getlist('create_project')
            update_project = request.POST.getlist('update_project')
            view_project = request.POST.getlist('view_project')
            delete_project = request.POST.getlist('delete_project')
            # Users
            create_users = request.POST.getlist('create_users')
            update_users = request.POST.getlist('update_users')
            view_users = request.POST.getlist('view_users')
            delete_users = request.POST.getlist('delete_users')
            print("soy users " + str(create_users))
            # Rol
            create_rol = request.POST.getlist('create_rol')
            update_rol = request.POST.getlist('update_rol')
            view_rol = request.POST.getlist('view_rol')
            delete_rol = request.POST.getlist('delete_rol')
            print("soy rol " + str(create_rol))

            # Para un permiso nuevo
            # Project
            if (view_project != []):
                print("project and view")
                can_view_project = Permission.objects.get(codename='view_project')
                group.permissions.add(can_view_project.id)
            if (create_project != []):
                can_create_project = Permission.objects.get(codename="add_project")
                group.permissions.add(can_create_project)
            if (update_project != []):
                can_change_project = Permission.objects.get(codename="change_project")
                group.permissions.add(can_change_project)
            if (delete_project != []):
                can_delete_project = Permission.objects.get(codename="delete_project")
                group.permissions.add(can_delete_project)

            # ROL
            if (view_rol != []):
                print("project and view")
                can_view_group = Permission.objects.get(codename='view_group')
                group.permissions.add(can_view_group.id)

            if (create_rol != []):
                print("proyecto1")
                can_add_rol = Permission.objects.get(codename='add_group')
                print(can_add_rol.id)
                group.permissions.add(can_add_rol.id)
                print("es vacio")
            if (update_rol != []):
                print("proyecto2")
                can_update_rol = Permission.objects.get(codename='change_group')
                print(can_update_rol.id)
                group.permissions.add(can_update_rol.id)
                print("es vacio")
            if (delete_rol != []):
                print("proyecto3")
                can_delete_rol = Permission.objects.get(codename='delete_group')
                print(can_delete_rol.id)
                group.permissions.add(can_delete_rol.id)
                print("es vacio")

            # Users

            if (view_users != []):
                print("project and view")
                can_view_users = Permission.objects.get(codename='view_users')
                group.permissions.add(can_view_users.id)
            if (create_users != []):
                print("usuario1")
                can_add_users = Permission.objects.get(codename='add_user')
                print(can_add_users.id)
                group.permissions.add(can_add_users.id)
                print("es vacio")
            if (update_users != []):
                print("usuario2")
                can_update_users = Permission.objects.get(codename='change_user')
                print(can_update_users.id)
                group.permissions.add(can_update_users.id)
                print("es vacio")
            if (delete_users != []):
                print("usuario3")
                can_delete_users = Permission.objects.get(codename='delete_user')
                print(can_delete_users.id)
                group.permissions.add(can_delete_users.id)
                print("es vacio")

            # Si quita la seleccion de uno de los permisos
            #Project
            if create_project == []:

                existPermissions = group.permissions.filter(codename="add_project")
                if existPermissions:
                    p = Permission.objects.get(codename="add_project")
                    p.group_set.remove(group)

            if view_project == []:
                existPermissions = group.permissions.filter(codename="view_project")
                if existPermissions:
                    p = Permission.objects.get(codename="view_project")
                    p.group_set.remove(group)

            if update_project == []:
                existPermissions = group.permissions.filter(codename="change_project")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="change_project")
                    p.group_set.remove(group)

            if delete_project == []:
                existPermissions = group.permissions.filter(codename="delete_project")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="delete_project")
                    p.group_set.remove(group)
            #Users

            if create_users == []:
                existPermissions = group.permissions.filter(codename="add_user")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="add_user")
                    p.group_set.remove(group)

            if view_users == []:
                existPermissions = group.permissions.filter(codename="view_users")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="view_users")
                    p.group_set.remove(group)

            if update_users == []:
                existPermissions = group.permissions.filter(codename="change_user")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="change_user")
                    p.group_set.remove(group)

            if delete_users == []:
                existPermissions = group.permissions.filter(codename="delete_user")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="delete_user")
                    p.group_set.remove(group)
            #Rol

            if create_rol == []:
                existPermissions = group.permissions.filter(codename="add_group")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="add_group")
                    p.group_set.remove(group)

            if view_rol == []:
                existPermissions = group.permissions.filter(codename="view_group")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="view_group")
                    p.group_set.remove(group)

            if update_rol == []:
                existPermissions = group.permissions.filter(codename="change_group")
                print(existPermissions)
                if existPermissions:
                    p = Permission.objects.get(codename="change_group")
                    p.group_set.remove(group)

            if delete_rol == []:
                print("soy delete")
                existPermissions = group.permissions.filter(codename="delete_group")
                print(existPermissions)
                if existPermissions:
                    print("deleteeeeeeee")
                    p = Permission.objects.get(codename="delete_group")
                    p.group_set.remove(group)



            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            messages.error(request, "Introduzca un rol válido")
            return HttpResponseRedirect(reverse_lazy('role'))

def ViewRole(request):
    name = request.GET.get('name', None)
    role = Group.objects.get(name = name)
    all_permissions = role.permissions.all()
    array_permissions=[]
    for i in all_permissions:
        array_permissions.append(i.codename)

    data = {
        'permissions': array_permissions
    }
    return JsonResponse(data)








