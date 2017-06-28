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

class Home(TemplateView):
    template_name = 'index.html'

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
        post_values = request.POST.copy()
        form = UserForm(post_values)

        form1 = UserForm()

        creator_choice=[(i.id, i.name) for i in Group.objects.all()]
        rol = forms.ChoiceField(
        required=True,
        choices=creator_choice
    )
        form1.fields['rol'].choices = creator_choice

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

            context = {'form': form}
            messages.success(request, "El usuario ha sido guardado exitosamente")
            return render(request, 'page-new-user.html', context)
        else:
            return render(request, 'page-new-user.html', {'form': form})

def DeleteUser(request,id):
    user = profileUser.objects.get(pk=id)
    print(user.user)
    user_pk = User.objects.get(username=user.user)
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
        print("en post")
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
                messages.success(request, 'La contraseña ha sido cambiada con éxito')
                return render(request, 'page-login.html',
                              {'form': form})
            else:
                print("else")
                form.add_error(None,'Las contraseñas no coinciden, por favor verifíque')
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
        print("en post update")
        post_values = request.POST.copy()
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



