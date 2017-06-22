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

class New_Users(FormView):
    template_name = 'page-new-user.html'
    form_class = ProfileForm

    def post(self, request, *args, **kwargs):
        print("en post")
        post_values = request.POST.copy()
        form = ProfileForm(request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            #user.is_active = False
            role= post_values['role']
            group= Group.objects.get(pk=role)
            phone = post_values['phone']
            new_user = profileUser(user= user, role=group, phone=phone)

           # group = Group.objects.get(name="Clientes")

            # try:
            #     activation_key = create_token()
            #     while UserProfile.objects.filter(activation_key=activation_key).count() > 0:
            #         activation_key = create_token()
            #     c = {'usuario': user.get_full_name,
            #          'key': activation_key,
            #          'host': request.META['HTTP_HOST']}
            #     subject = 'Aplicación Prueba - Activación de cuenta'
            #     message_template = 'success.html'
            #     email = user.email
            #     send_email(subject, message_template, c, email)
            # except:
            #     form.add_error(
            #         None, "Hubo un error en la conexión intente registrarse de nuevo. Gracias")
            #     context = {'form': form, 'host': request.get_host()}
            #     return render(request, 'register.html', context)

            user.save()
            new_user.save()
            #user.groups.add(group)
           # key_expires = datetime.datetime.today() + datetime.timedelta(days=1)
            #user_profile = UserProfile(user=user, activation_key=activation_key,
                  #                     key_expires=key_expires)
           # user_profile.save()
            context = {'form':form}
            messages.success(request,"El usuario ha sido guardado exitosamente")
            return render(request, 'page-new-user.html', context)
        else:
            return render(request, 'page-new-user.html', {'form': form})


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





