# -*- coding: utf-8 -*-
import hashlib
import random
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import *
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.models import Project, Project_user
from users.forms import *
from users.models import *
from django.urls import reverse

class Login(TemplateView):
    template_name = 'page-login.html'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
               
            error_username = "Tu username/email o contraseña no son correctos."

            user_auth = authenticate_user(username)
            print("esto es user_auth")
            print(user_auth)
            if user_auth is not None:
        
                if user_auth.is_active:
                    user = authenticate(username=user_auth.username,
                                        password=password)
                    print("user login")
                    print(user)
                    if user:
                        login(request, user)
                        return HttpResponseRedirect(reverse_lazy('project'))
                    else:
                        form.add_error(None, error_username)
                        return render(request, 'page-login.html',
                                      {'form': form})
                else:
                    print("no active")
                    new_user = profileUser.objects.get(user=user_auth.pk)
                    print(new_user)
                    activation_key = new_user.activation_key
                    if password == activation_key:
                        print("son iguales")
                        return HttpResponseRedirect(reverse('first_session', 
                            kwargs={'activation_key': activation_key}))
                    else:
                        form.add_error(None, error_username)
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

class Users(TemplateView):
    template_name = 'page-user.html'

    def get_context_data(self, **kwargs):
        context = super(
            Users, self).get_context_data(**kwargs)
        user = profileUser.objects.all()
        context['users'] = user
        return context

class New_Users(FormView):
    template_name = 'page-new-user.html'
    form_class = UserForm
  

    def get_context_data(self, **kwargs):
        context = super(
            New_Users, self).get_context_data(**kwargs)
        context['title'] = 'Agregar'

        return context

    def post(self, request, *args, **kwargs):
        print("en post new user")
        post_values = request.POST.copy()
        form = UserForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            activation_key = create_token()
            user.set_password(activation_key)
            user.is_active = 0
            user.save()
            user_pk = User.objects.get(id=user.id)
            role= post_values['rol']
            group= Group.objects.get(pk=role)
            user.groups.add(group)
            phone = post_values['phone']
            new_user = profileUser(user = user_pk, phone=phone, activation_key=activation_key)
            new_user.save()
            new_user_pk= profileUser.objects.get(id=new_user.pk)
            print('new_user ')
            print(new_user_pk.pk)
            proj1 = request.POST.get('project',None)
            print(proj1)
            proj2 = proj1.split(', ')
            print("esto es split")
            print(proj2)
            for i in proj2:
                proj = Project.objects.filter(name=i).exists()
                print(proj)
                if proj:
                    print('el proyecto '+ str(i) + ' existe')
                    proj_exist= Project.objects.get(name=i)
                    print(proj_exist.pk)
                    project_user = Project_user(project=proj_exist, user = new_user_pk)
                    project_user.save()
                else:
                    if i != '':
                        print('el proyecto '+ str(i) + ' no existe')
                        code = codeProject(i)
                        print(code)
                        new_project = Project(code=code, name=i)
                        new_project.save()
                        proj_exist = Project.objects.get(name=i)
                        project_user = Project_user(project=proj_exist, user=new_user_pk)
                        project_user.save()

            c = {'usuario': user.first_name,
                    'username':user.username,
                    'key': activation_key,
                    'host': request.META['HTTP_HOST']}

            email_subject = 'IDBC Group - Activación de cuenta'
            message_template = 'emailNewUser.html'
            email = user.email
            send_email(email_subject, message_template, c, email)

            # new_user.save()
            # user.groups.add(group)
            # key_expires = datetime.datetime.today() + datetime.timedelta(days=1)

            messages.success(request, "El usuario ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('users'))
        else:
            messages.success(request, 'Error al registrar usuario')
            return HttpResponseRedirect(reverse_lazy('new_users'))

def DeleteUser(request,id):
    user = profileUser.objects.get(pk=id)
    print(user.user)
    user_pk = User.objects.get(pk=user.user.pk)
    user.delete()
    user_pk.delete()
    messages.success(request, "El usuario " + str(user.user.username) +" se ha eliminado exitosamente")
    return HttpResponseRedirect(reverse_lazy('users'))

def send_email(subject, message_template, context, email):
    from_email = 'IDBC Group - Activación de cuenta'
    email_subject = subject
    message = get_template(message_template).render(context)
    msg = EmailMessage(email_subject, message, to=[email], from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

def create_token():
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
    random.shuffle(chars)
    chars = ''.join(chars)
    sha1 = hashlib.sha1(chars.encode('utf8'))
    token = sha1.hexdigest()
    key = token[:12]
    return key

class First_Session(TemplateView):
    template_name = 'first_session.html'

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = FirstSessionForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            activation_key = self.kwargs['activation_key']
            user = profileUser.objects.get(activation_key=activation_key)
            username = User.objects.get(pk = user.user.pk)
            print(username.pk)
            print(activation_key)
            password = post_values['password']
            password2 = post_values['password2']
            print(password2)

            if password == password2:
                username.set_password(password)
                username.is_active= 1
                print(username.is_active)
                print(username.password)
                username.save()
                form.add_error(None, 'La contraseña ha sido cambiada con éxito')
                return render(request, 'page-login.html',
                              {'form': form})
            else:
                print("else")
                form.add_error(None,'Las contraseñas no coinciden, por favor verifíque')
                return render(request, 'first_session.html',
                              {'form': form})
        else:
            return render(request, 'first_session.html',
                          {'form': form})

class Update_Users(TemplateView):
    template_name = 'page-new-user.html'
    form_class = UpdateUserForm

    def get_context_data(self, **kwargs):
        context = super(
            Update_Users, self).get_context_data(**kwargs)

        context['title'] = 'Modificar'
        user = profileUser.objects.get(pk=self.kwargs['id'])
        print("users")
        print(self.kwargs['id'])
        print(user)

        data = {'first_name': user.user.first_name,
                 'last_name': user.user.last_name,
                 'username': user.user.username,
                 'rol': user.user.groups.all()[0],
                 'email' : user.user.email,
                'phone': user.phone }
        form = UserForm(initial=data)
        context['userProfile'] = user
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(data=request.POST, instance=request.user)
        #form.fields['username'].required = False
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user_pk = kwargs['id']
            userProfile = profileUser.objects.get(pk=user_pk)
            print(userProfile.user)
            user = User.objects.get(username=userProfile.user)
            print(user)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            userProfile.phone = request.POST['phone']
            user.username = request.POST['username']
            user.save()
            userProfile.save()
            role = request.POST['rol']
            group = Group.objects.get(pk=role)
            user.groups.remove(userProfile.user.groups.all()[0])
            user.groups.add(group)
            user.save()
            messages.success(request, "El usuario ha sido modificado con éxito")
            return HttpResponseRedirect(reverse_lazy('users'))

        else:
            return render(request, 'page-user.html',
                              {'form': form})

class Password_Reset(TemplateView):
    template_name = 'password-reset-form.html'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = PasswordResetForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            email = post_values['email']
            print(email)
            user = User.objects.filter(email=email).exists()
            print(user)
            if user:
                print("en if")
                username = User.objects.get(email = email)
                print(username.is_active)
                if username.is_active:
                    user = profileUser.objects.get(user=username)
                    print(user)
                    user.activation_key = create_token()
                    print("user.activation")
                    print(user.activation_key)
                    user.save()

                    c = {'usuario': username.first_name,
                        'username':username,
                        'key': user.activation_key,
                        'host': request.META['HTTP_HOST']
                    }

                    email_subject = 'IDBC Group - Recuperación de Contraseña'
                    message_template = 'password-reset-email.html'
                    email = email
                    send_email(email_subject, message_template, c, email)
                    return render(request, 'password-reset-done.html')
                else:
                    form.add_error(None, 'Lo sentimos, debe activar la cuenta')
                    return render(request, 'page-login.html',
                                  {'form': form})

            else :
                print("else no user")
                form.add_error(None, 'El correo ingresado no es válido, por favor verifique')
                return render(request, 'password-reset-form.html',
                              {'form': form})
        else:
            print("form is not valid")
            form.add_error(None, 'Ingrese un correo electrónico válido')
            return render(request,'password-reset-form.html',
                          {'form':form})

class Password_Reset_Confirm(TemplateView):
    template_name = 'password-reset-confirm.html'

    def post(self, request, *args, **kwargs):
        print("post reset")
        post_values = request.POST.copy()
        form = FirstSessionForm(post_values)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            activation_key = self.kwargs['token']
            print(activation_key)
            user = profileUser.objects.get(activation_key=activation_key)
            print(user)
            username = User.objects.get(pk=user.user.pk)
            print(username.pk)
            print(activation_key)
            password = post_values['password']
            password2 = post_values['password2']
            print(password)
            print(password2)
            if password == password2:
                print("las claves son iguales")
                username.set_password(password)
                form.add_error(None, "Las contraseña se ha restablecido exitosamente.")
                return render(request, 'page-login.html', {'form':form})
            else:
                print("else")
                messages.success(request, 'Las contraseñas no coinceden, por favor verifique.')
                return HttpResponseRedirect(reverse_lazy('password_reset_confirm',
                                                         kwargs={'token': activation_key}))
        else:
            #form.add_error(None,'Se ha producido un error ')
            return render(request, 'password-reset-confirm.html', {'form':form, 'token':self.kwargs['token']})


class Profile(TemplateView):
    template_name = 'page-profile.html'
    form_class = UpdateProfileForm

    def get_context_data(self, **kwargs):
        context = super(
            Profile, self).get_context_data(**kwargs)
        print("get")

        print(self.kwargs['id'])

        user = profileUser.objects.get(user_id=self.kwargs['id'])
        #print(user)
        #if not user:
         #   data = {
          #      'first_name': User.first_name,
           #     'last_name' : User.last_name
            #}
        #else:
        data = {'first_name': user.user.first_name,
                 'last_name': user.user.last_name,
                 'username': user.user.username,
                 'rol': user.user.groups.all()[0],
                 'email' : user.user.email,
                'phone': user.phone,
                'image_profile': user.image_profile
                 }
        form = UserForm(initial=data)
        context['form'] = form
        context['users']=user
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            user_pk = kwargs['id']
            userProfile = profileUser.objects.get(user=user_pk)
            print(userProfile.user.id)
            user = User.objects.get(pk=userProfile.user_id)
            print(user)
            user.first_name = request.POST['first_name']
            print(user.first_name)
            user.last_name = request.POST['last_name']
            userProfile.phone = request.POST['phone']
            if (request.FILES == {}):
                pass
            else:
                userProfile.image_profile = request.FILES['image_profile']
                userProfile.load_photo = True

            print(userProfile.image_profile)
            user.username = request.POST['username']
            user.save()
            userProfile.save()
            messages.success(request, "Su perfil ha sido actualizado exitosamente")
            return HttpResponseRedirect(reverse_lazy('profile',
                                                     kwargs={'id': user_pk}))

        else:
            return render(request, 'page-profile.html',
                          {'form': form})


def codeProject(name):
    name = ''.join(name)
    return name[:3]

def get_projects(request):
    q = request.GET.get('term', '')
    projects = Project.objects.filter(name__icontains = q )[:20]
    print(projects)
    results = []
    for project in projects:
        project_json = {}
        project_json['id'] = project.code
        project_json['label'] = project.name
        project_json['value'] = project.name
        results.append(project_json)
    print(results)
    return JsonResponse(results, safe=False)

