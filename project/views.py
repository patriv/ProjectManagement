# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.forms import *

class Login(TemplateView):
    template_name = 'page-login.html'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = request.POST['username']
            print(username)
            password = request.POST['password']
            print(password)
            user_auth = authenticate_user(username, password)
            if user_auth is not None:
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse_lazy('project'))
                    else:
                        messages.error(request, "Lo sentimos, su correo o contraseña no son correctos")
                        return render(request, 'page-login.html',
                                      {'form': form})
                else:
                    messages.error(request, "Aún no has confirmado tu correo.")
                    return render(request, 'page-login.html',
                                  {'form': form})
            else:
                messages.error(request, "Lo sentimos, su correo o contraseña no son correctos.")
                return render(request, 'page-login.html',
                              {'form': form})
        else:
            context = {'form': form}
            return render(request, 'page-login.html', context)



def authenticate_user(username=None, password=None):
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

class Role(TemplateView):
    template_name = 'page-role.html'
