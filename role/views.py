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

'''
Clase que muestra los roles del sistema
'''

class Role(TemplateView):
    template_name = 'page-role.html'

    '''
    Función que GET que muestra los roles del sistema
    '''
    def get_context_data(self, **kwargs):
        context = super(
            Role, self).get_context_data(**kwargs)
        role=Group.objects.all()
        context['roles'] = role
        return context


'''
Clase para agregar nuevos roles al sistema
'''
class AddRole(FormView):
    template_name= 'page-role.html'
    form_class = RoleForm   

    '''
    Función POST para el envío del formulario
    '''

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = RoleForm(post_values)
        if form.is_valid():
            newRole = form.save(commit=False)
            '''
            Se obtiene el nombre del rol introducido por el usuario
            '''
            newRole.name = post_values['name']
            '''
            Condicional que verifica si el nombre introducido del rol ya está guardado en la base de datos
            '''
            if Group.objects.filter(name=newRole.name).exists():
                messages.error(request, "Este rol ya existe, por favor verifique")
                return HttpResponseRedirect(reverse_lazy('role'))
            newRole.save()
            '''
            Se obtiene el nombre del rol guardado en la base de datos con la finalidad de asociarle los permisos 
            correspondientes.
            '''
            group = Group.objects.get(name = newRole.name)

            '''
            Se toman los permisos seleccionados por el usuario relacionados con los proyectos
            '''
            create_project = request.POST.getlist('create_project')
            update_project = request.POST.getlist('update_project')
            view_project = request.POST.getlist('view_project')
            delete_project = request.POST.getlist('delete_project')

            '''
            Se toman los permisos seleccionados por el usuario relacionados con los usuarios
            '''
            create_users = request.POST.getlist('create_users')
            update_users = request.POST.getlist('update_users')
            view_users = request.POST.getlist('view_users')
            delete_users = request.POST.getlist('delete_users')

            '''
            Se toman los permisos seleccionados por el usuario relacionados con los roles
            '''
            create_rol = request.POST.getlist('create_rol')
            update_rol = request.POST.getlist('update_rol')
            view_rol = request.POST.getlist('view_rol')
            delete_rol = request.POST.getlist('view_rol')

            '''
            Condicional que verifica y guarda si el rol introducido puede ver proyectos
            '''
            if  (view_project != []):
                '''
                En caso de no existir este permiso en la tabla Pemission, se crea primero para luego asociarlo al rol
                '''
                if not (Permission.objects.filter(codename='view_project').exists()):
                    content_type = ContentType.objects.get(app_label='project', model='project')
                    permission = Permission.objects.create(codename='view_project',
                                                           name='Can view Project',
                                                           content_type=content_type)
                can_view_project = Permission.objects.get(codename='view_project')
                '''
                Se asocia el permiso de ver proyecto con el respectivo rol
                '''
                group.permissions.add(can_view_project.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede crear proyectos
            '''
            if (create_project != []):
                can_create_project = Permission.objects.get(codename="add_project")
                group.permissions.add(can_create_project)
            '''
            Condicional que verifica y guarda si el rol introducido puede modificar proyectos
            '''
            if (update_project != []):
                can_change_project = Permission.objects.get(codename="change_project")
                group.permissions.add(can_change_project)

            '''
            Condicional que verifica y guarda si el rol introducido puede eliminar proyectos
            '''
            if (delete_project != []):
                can_delete_project = Permission.objects.get(codename="delete_project")
                group.permissions.add(can_delete_project)

            '''
            Condicional que verifica y guarda si el rol introducido puede ver roles
            '''
            if (view_rol != []):
                '''
                En caso de no existir este permiso en la tabla Pemission, se crea primero para luego asociarlo al rol
                '''
                if not (Permission.objects.filter(codename='view_group').exists()):
                    content_type = ContentType.objects.get(app_label='auth', model='group')
                    permission = Permission.objects.create(codename='view_group',
                                                           name='Can view group',
                                                           content_type=content_type)
                can_view_group = Permission.objects.get(codename='view_group')
                '''
                Se asocia el permiso de ver rol con el respectivo rol
                '''
                group.permissions.add(can_view_group.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede crear roles
            '''
            if (create_rol !=[]):
                can_add_rol = Permission.objects.get(codename = 'add_group')
                group.permissions.add(can_add_rol.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede modificar roles
            '''
            if (update_rol != []):
                can_update_rol = Permission.objects.get(codename='change_group')
                group.permissions.add(can_update_rol.id)
            '''
            Condicional que verifica y guarda si el rol introducido puede eliminar roles
            '''
            if  (delete_rol != []):
                can_delete_rol = Permission.objects.get(codename='delete_group')
                group.permissions.add(can_delete_rol.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede ver usuarios
            '''
            if (view_users != []):
                '''
                En caso de no existir este permiso en la tabla Pemission, se crea primero para luego asociarlo al rol
                '''
                if not (Permission.objects.filter(codename='view_users').exists()):
                    content_type = ContentType.objects.get(app_label='auth', model='user')
                    permission = Permission.objects.create(codename='view_users',
                                                           name='Can View Users',
                                                           content_type=content_type)
                can_view_users = Permission.objects.get(codename='view_users')
                group.permissions.add(can_view_users.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede crear usuarios
            '''
            if (create_users !=[]):
                can_add_users = Permission.objects.get(codename = 'add_user')
                group.permissions.add(can_add_users.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede modificar usuarios
            '''
            if (update_users != []):
                can_update_users = Permission.objects.get(codename='change_user')
                group.permissions.add(can_update_users.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede eliminar usuarios
            '''
            if (delete_users != []):
                can_delete_users = Permission.objects.get(codename='delete_user')
                group.permissions.add(can_delete_users.id)

            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            return HttpResponseRedirect(reverse_lazy('role'))

'''
Función que elimina un rol.
@:param request 
@:param id: identificador del rol a eliminar
@:return redirecciona a la página de roles
'''
def DeleteRole(request,id):
    role = Group.objects.get(pk=id)
    user = role.user_set.exists()
    '''
    En caso de que el rol tenga asociado a usarios, no se puede eliminar.
    '''
    if user:
        messages.success(request, "El rol "+str(role.name)+ " no se puede eliminar, tiene usuarios asociados.")
        return  HttpResponseRedirect(reverse_lazy('role'))

    else:
        role.delete()
        messages.success(request, "El rol " + str(role.name) +" se ha eliminado exitosamente")
        return HttpResponseRedirect(reverse_lazy('role'))

'''
Clase que permite modificar un rol
'''
class UpdateRole(UpdateView):
    template_name = 'page-role.html'
    form_class = RoleForm

    '''
    Función POST para el envío del formulario
    '''
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = RoleForm(post_values)
        if form.is_valid():
            pk = kwargs['id']
            group = Group.objects.get(id = pk)
            group.name = request.POST['name']
            '''
            Se obtienen todos los roles excluyendo el intoroducido por el usuario. Se guardan en una lista
            '''
            ex = Group.objects.exclude(pk=pk)
            others =[]
            for i in ex:
                others.append(i.name)
            '''
            Si aparece alguna ocurrencia del nombre introducido por el usuario, quiere decir que este rol ya existe.
            Se envía un mensaje al usuario.
            '''
            if others.count(group.name) != 0:
                messages.error(request, "Este rol ya existe, por favor verifique")
                return HttpResponseRedirect(reverse_lazy('role'))
            group.save()

            '''
            Se obtienen los permisos seleccionados por el usuario de proyectos
            '''
            create_project = request.POST.getlist('create_project')
            update_project = request.POST.getlist('update_project')
            view_project = request.POST.getlist('view_project')
            delete_project = request.POST.getlist('delete_project')

            '''
            Se obtienen los permisos seleccionados por el usuario de usuarios
            '''
            create_users = request.POST.getlist('create_users')
            update_users = request.POST.getlist('update_users')
            view_users = request.POST.getlist('view_users')
            delete_users = request.POST.getlist('delete_users')

            '''
            Se obtienen los permisos seleccionados por el usuario de roles
            '''
            create_rol = request.POST.getlist('create_rol')
            update_rol = request.POST.getlist('update_rol')
            view_rol = request.POST.getlist('view_rol')
            delete_rol = request.POST.getlist('delete_rol')

            '''
            En caso de que el usuario quiera agregar un nuevo permiso al rol a modificar.
            Ver proyecto
            '''
            if (view_project != []):
                if not (Permission.objects.filter(codename='view_project').exists()):
                    content_type = ContentType.objects.get(app_label='project', model='project')
                    permission = Permission.objects.create(codename='view_project',
                                                           name='Can view Project',
                                                           content_type=content_type)
                can_view_project = Permission.objects.get(codename='view_project')
                group.permissions.add(can_view_project.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede crear proyecto
            '''
            if (create_project != []):
                can_create_project = Permission.objects.get(codename="add_project")
                group.permissions.add(can_create_project)

            '''
            Condicional que verifica y guarda si el rol introducido puede modificar proyecto
            '''
            if (update_project != []):
                can_change_project = Permission.objects.get(codename="change_project")
                group.permissions.add(can_change_project)

            '''
            Condicional que verifica y guarda si el rol introducido puede eliminar proyecto
            '''
            if (delete_project != []):
                can_delete_project = Permission.objects.get(codename="delete_project")
                group.permissions.add(can_delete_project)

            '''
            Condicional que verifica y guarda si el rol introducido puede ver rol
            '''
            if (view_rol != []):
                if not (Permission.objects.filter(codename='view_group').exists()):
                    content_type = ContentType.objects.get(app_label='auth', model='group')
                    permission = Permission.objects.create(codename='view_group',
                                                           name='Can view group',
                                                           content_type=content_type)
                can_view_group = Permission.objects.get(codename='view_group')
                group.permissions.add(can_view_group.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede crear rol
            '''
            if (create_rol != []):
                can_add_rol = Permission.objects.get(codename='add_group')
                group.permissions.add(can_add_rol.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede modificar rol
            '''
            if (update_rol != []):
                can_update_rol = Permission.objects.get(codename='change_group')
                group.permissions.add(can_update_rol.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede eliminar rol
            '''
            if (delete_rol != []):
                can_delete_rol = Permission.objects.get(codename='delete_group')
                group.permissions.add(can_delete_rol.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede ver usuarios
            '''
            if (view_users != []):
                if not (Permission.objects.filter(codename='view_users').exists()):
                    content_type = ContentType.objects.get(app_label='auth', model='user')
                    permission = Permission.objects.create(codename='view_users',
                                                           name='Can View Users',
                                                           content_type=content_type)
                can_view_users = Permission.objects.get(codename='view_users')
                group.permissions.add(can_view_users.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede crear usuarios
            '''
            if (create_users != []):
                can_add_users = Permission.objects.get(codename='add_user')
                group.permissions.add(can_add_users.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede modificar usuarios
            '''
            if (update_users != []):
                can_update_users = Permission.objects.get(codename='change_user')
                group.permissions.add(can_update_users.id)

            '''
            Condicional que verifica y guarda si el rol introducido puede eliminar usuarios
            '''
            if (delete_users != []):
                can_delete_users = Permission.objects.get(codename='delete_user')
                group.permissions.add(can_delete_users.id)

            '''
            En caso de que el usuario quite uno de los permisos que ya tenía asociado el rol a modificar
            '''

            '''
            Elimina la asociación del rol con el permiso de crear proyecto
            '''
            if create_project == []:

                existPermissions = group.permissions.filter(codename="add_project")
                if existPermissions:
                    p = Permission.objects.get(codename="add_project")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de ver proyecto
            '''
            if view_project == []:
                existPermissions = group.permissions.filter(codename="view_project")
                if existPermissions:
                    p = Permission.objects.get(codename="view_project")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de modificar proyecto
            '''
            if update_project == []:
                existPermissions = group.permissions.filter(codename="change_project")
                if existPermissions:
                    p = Permission.objects.get(codename="change_project")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de eliminar proyecto
            '''
            if delete_project == []:
                existPermissions = group.permissions.filter(codename="delete_project")
                if existPermissions:
                    p = Permission.objects.get(codename="delete_project")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de crear usuarios
            '''
            if create_users == []:
                existPermissions = group.permissions.filter(codename="add_user")
                if existPermissions:
                    p = Permission.objects.get(codename="add_user")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de ver usuarios
            '''
            if view_users == []:
                existPermissions = group.permissions.filter(codename="view_users")
                if existPermissions:
                    p = Permission.objects.get(codename="view_users")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de modificar usuarios
            '''
            if update_users == []:
                existPermissions = group.permissions.filter(codename="change_user")
                if existPermissions:
                    p = Permission.objects.get(codename="change_user")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de eliminar usuarios
            '''
            if delete_users == []:
                existPermissions = group.permissions.filter(codename="delete_user")
                if existPermissions:
                    p = Permission.objects.get(codename="delete_user")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de crear rol
            '''
            if create_rol == []:
                existPermissions = group.permissions.filter(codename="add_group")
                if existPermissions:
                    p = Permission.objects.get(codename="add_group")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de ver rol
            '''
            if view_rol == []:
                existPermissions = group.permissions.filter(codename="view_group")
                if existPermissions:
                    p = Permission.objects.get(codename="view_group")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de modificar rol
            '''
            if update_rol == []:
                existPermissions = group.permissions.filter(codename="change_group")
                if existPermissions:
                    p = Permission.objects.get(codename="change_group")
                    p.group_set.remove(group)

            '''
            Elimina la asociación del rol con el permiso de eliminar rol
            '''
            if delete_rol == []:
                existPermissions = group.permissions.filter(codename="delete_group")
                if existPermissions:
                    p = Permission.objects.get(codename="delete_group")
                    p.group_set.remove(group)
            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            messages.error(request, "Introduzca un rol válido")
            return HttpResponseRedirect(reverse_lazy('role'))

'''
Función creada para pasar a un JQuery a través de un JSON la información de los roles con sus respectivos permisos.
'''
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








