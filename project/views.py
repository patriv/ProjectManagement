# -*- coding: utf-8 -*-
import hashlib
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.forms import *
from project.models import *


class Login(TemplateView):
    template_name = 'page-login.html'
    print("hello:")

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            #user_pk = User.objects.get(username=username)
            # print(user_pk.password)
            #


            
            error_username = "Tu username/email o contraseña no son correctos."

            user_auth = authenticate_user(username)
            print("esto es user_auth")
            print(user_auth)
            if user_auth is not None:
                print("clave")
                passwordUser = user_auth.password
                print(passwordUser)

                if (passwordUser == ""):
                    user_profile = profileUser.objects.get(user=user_auth.pk)
                    print(user_profile)
                    user_profile_password = user_profile.activation_key
                    print("dentro de if")
                    print(user_profile_password)
                    print(password)
                    if(user_profile_password == password):
                        print("tengo que crear la vista")
                        return HttpResponseRedirect(reverse_lazy('change_password'))
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
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(
            New_Users, self).get_context_data(**kwargs)
        role = Group.objects.all()
        context['roles']=role
        return context

    def post(self, request, *args, **kwargs):
        print("en post")
        post_values = request.POST.copy()
        form = UserForm(post_values)
        if form.is_valid():
            user = form.save(commit=False)
            activation_key = create_token()
            user.set_password(activation_key)
            user.save()
            print(user.pk)
            print(user.password)
            user_pk = User.objects.get(id=user.id)
            print("user_pk.passwrd" + " "+ str(user_pk.password))
            role= post_values['rol']
            print("soy rol")
            print(role)
            group= Group.objects.get(pk=role)
            user.groups.add(group)
            phone = post_values['phone']
            new_user = profileUser(user = user_pk, phone=phone, activation_key=activation_key)
            print("antes de guardar new_user")
            new_user.save()

            c = {'usuario': user.first_name,
                             'key': activation_key,
                             'host': request.META['HTTP_HOST']}

            from_email = 'projectidbcgroup@gmail.com'
            email_subject = 'IDBC Group - Activación de cuenta'
            message_template = 'emailNewUser.html'
            email = user.email
            send_email(email_subject, message_template, c, email)

            # while profileUser.objects.filter(activation_key=activation_key).count() > 0:
            #     activation_key = create_token()
            #     c = {'usuario': user.get_full_name,
            #          'key': activation_key,
            #          'host': request.META['HTTP_HOST']}
            #     subject = 'Aplicación Prueba - Activación de cuenta'
            #     message_template = 'success.html'
            #     email = user.email
            #     send_email(subject, message_template, c, email)


            # new_user.save()
            # user.groups.add(group)
            # key_expires = datetime.datetime.today() + datetime.timedelta(days=1)

            context = {'form': form}
            messages.success(request, "El usuario ha sido guardado exitosamente")
            return render(request, 'page-new-user.html', context)
        else:
            return render(request, 'page-new-user.html', {'form': form})

def send_email(subject, message_template, context, email):
    from_email = 'IDBC Group - Activación de cuenta'
    email_subject = subject
    message = get_template(message_template).render(context)
    msg = EmailMessage(email_subject, message, to=[email], from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    print("Se envió exitosamente el correo.")



def create_token():
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
    random.shuffle(chars)
    chars = ''.join(chars)
    sha1 = hashlib.sha1(chars.encode('utf8'))
    token = sha1.hexdigest()
    key = token[:12]
    return key

# def first_session(request, id):
#     user = User.objects.get(pk=id)
#     print(user)
#     user_profile = profileUser.objects.get(user=user) 



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





# class UserRegistration(TemplateView):
#     template_name = 'signup.html'

#     def get_context_data(self, **kwargs):
#         context = super(UserRegistration, self).get_context_data(**kwargs)
#         context['states'] = Estado.objects.all()
#         context['formulario1'] = UserForm()
#         context['telfform'] = CelularForm()
#         context['formulario2'] = DireccionForm()
#         # TEMPORAL
#         context['mentorform'] = MentorForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         post_values = request.POST.copy()
#         userForm = UserForm(post_values)
#         direcForm = DireccionForm(post_values)
#         userattrForm = CelularForm(post_values)

#         # TEMPORAL
#         userattrForm_temporal = MentorForm(post_values)

#         if userForm.is_valid() and direcForm.is_valid() and userattrForm.is_valid():
#             # User
#             new_user = userForm.save()
#             new_user.is_active = 0
#             new_user.set_password(post_values['password'])
#             new_user.save()

#             # salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
#             activation_key = "clubmercado" + str(new_user.id)
#             key_expires = datetime.datetime.today() + datetime.timedelta(2)
#             new_profile = UserProfile(user=new_user, activation_key=activation_key,
#                                       key_expires=key_expires)
#             new_profile.save()

#             # Direction
#             direction = direcForm.save()
#             # User Attributes
#             userattr = userattrForm.save(commit=False)
#             userattr.user = new_user
#             userattr.direccion = direction
#             userattr.mentor = User.objects.get(pk=int(post_values['mentor']))  ### MENTOR
#             userattr.save()
#             # User Group
#             UserGroup(user=new_user, group=Group.objects.get(id=1)).save()  ### CABLEADO

#             # Notifications
#             for x in ['1', '2', '3', '4', '5']:
#                 Notifications(notification_id=x, sms='t', email='t', user_id=new_user.id).save()

#             c = {'usuario': new_user.first_name,
#                  'key': activation_key,
#                  'host': request.META['HTTP_HOST']}
#             from_email = 'equipo@clubmercado.com'
#             email_subject = 'Club Mercado - Activación de cuenta'
#             message = get_template('correos/registro.html').render(c)
    #             msg = EmailMessage(email_subject, message, to=[new_user.email], from_email=from_email)
#             msg.content_subtype = 'html'
#             msg.send()

#             return HttpResponseRedirect('../../?msg=2')
#         else:
#             context = {
#                 'formulario1': userForm,
#                 'telfform': userattrForm,
#                 'formulario2': direcForm,
#                 'mentorform': userattrForm_temporal,
#                 'states': Estado.objects.all()

#             }
#             return render_to_response('signup.html', context,
# context_instance=RequestContext(request))