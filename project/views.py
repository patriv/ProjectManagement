# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.forms import *

class Login(TemplateView):
    template_name = 'page-login.html'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            error_username = "Tu username/email o contraseña no son correctos."
            user_auth = authenticate_user(username)
            if user_auth is not None:
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse_lazy('project'))
                    else:
                        form.add_error(None, error_username)
                        return render(request, 'page-login.html',
                                      {'form': form})
                else:
                    print("else")

                    #messages.error(request, "Aún no has confirmado tu correo.")
                    return render(request, 'page-login.html',
                                  {'form': form})
            else:
                form.add_error(None, error_username)
                return render(request, 'page-login.html',
                              {'form': form})
        else:
            context = {'form': form}
            return render(request, 'page-login.html', context)



def authenticate_user(username=None):
    try:
        user = User.objects.get(username=username)
        if user is not None:
            return user
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username)
            if user is not None:
                return user
        except User.DoesNotExist:
            return None


class Home(TemplateView):
    template_name = 'index.html'

class Users(TemplateView):
    template_name = 'page-user.html'

class New_Users(TemplateView):
    template_name = 'page-new-user.html'

class Update_Users(TemplateView):
    template_name = 'page-update-user.html'

class Forgot_Password(TemplateView):
    template_name = 'page-forgot-password.html'

class Change_Password(TemplateView):
    template_name = 'page-change-password.html'

class New_Project(TemplateView):
    template_name = 'page-new-project.html'

class Profile(TemplateView):
    template_name = 'page-profile.html'

class Update_Project(TemplateView):
    template_name = 'page-update-project.html'

class Detail_Project(TemplateView):
    template_name = 'page-detail-project.html'


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
        form = RoleForm(request.POST)
        if form.is_valid():
            newRole = form.save()
            print(newRole.pk)
            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            return HttpResponseRedirect(reverse_lazy('role'))


def DeleteRole(request,id):
    role = Group.objects.get(pk=id)
    role.delete()
    messages.success(request, "El rol " + str(role.name) +" se ha eliminado exitosamente")
    print("redireccion")
    return HttpResponseRedirect(reverse_lazy('role'))


class UpdateRole(FormView):
    template_name = 'page-role.html'
    form_class = RoleForm

    def get_context_data(self, **kwargs):
        print("en get")
        context = super(
            UpdateRole, self).get_context_data(**kwargs)
        context['title'] = 'Editar'

        role= Group.objects.get(pk=self.kwargs['id'])
        print(role)
        data ={
            'name': role.name
        }
        form = RoleForm(initial=data)
        print(form)
        context['roles']=form
        return context


    def post(self, request, *args, **kwargs):
        print("e post")
        post_values = request.POST.copy()
        form = RoleForm(post_values)
        print(form.is_valid())

        if form.is_valid():
            pk = kwargs['id']
            role = Group.objects.get(id = pk)
            role.name = request.POST['name']
            role.save()
            messages.success(request, "Su rol se ha guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('role'))
        else:
            return HttpResponseRedirect(reverse_lazy('role'))





