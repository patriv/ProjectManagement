# -*- coding: utf-8 -*-
import hashlib
import random
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render
from project.models import Project, ProjectUser
from task.models import Task
from users.forms import *
from users.models import *
from django.urls import reverse

'''
Clase que muestra la vista principal del sistme.Login
'''
class Login(TemplateView):
    template_name = 'page-login.html'

'''
Función que permite a un usuario iniciar sesión
'''
def user_login(request):
    '''
    Si hay una sesión iniciada y se trata de acceder nuevamente, se cierra ésta y se debe iniciar nuevamente.
    '''
    if request.user.is_authenticated():
        #messages.success(request, 'Error al registrar usuario')
        return HttpResponseRedirect(reverse_lazy('logout'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            error_username = "Tu username/email o contraseña no son correctos."

            user_auth = authenticate_user(username)
            '''
            Condicional que verifica que el usuario exista en la base de datos
            '''
            if user_auth is not None:
                '''
                En caso de que el usuario esté como activo ingresa de manera exitosa al sistema
                '''
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
                # En caso de que el usuario esté no activo, se lleva a la vista de cambio de contraseña
                else:
                    new_user = ProfileUser.objects.get(fk_profileUser_user=user_auth.pk)
                    activation_key = new_user.activationKey
                    '''
                    En caso de que la clave introducida sea la asignada por primera vez de manera aleatoria, se lleva al 
                    usuario al cambio de contraseña.
                    '''
                    if password == activation_key:
                        return HttpResponseRedirect(reverse('first_session',
                                                            kwargs={'activationKey': activation_key}))
                    else:
                        form.add_error(None, error_username)
                        return render(request, 'page-login.html',
                                      {'form': form})

            else:

                form.add_error(None, error_username)
                return render(request, 'page-login.html',
                              {'form': form})
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'page-login.html', context)

'''
Función que permite autenticar a un usuario bien sea por username o por correo electrónico
@:param username: username o email del usuario.
'''
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


'''
Clase que permite visualizar a todos los usuarios registrados en el sistema.
'''
class Users(TemplateView):
    template_name = 'page-user.html'

    def get_context_data(self, **kwargs):
        context = super(
            Users, self).get_context_data(**kwargs)
        user = ProfileUser.objects.all()
        context['users'] = user
        return context

'''
Clase que permite agregar un nuevo usuario al sistema
'''
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
        if form.is_valid():
            user = form.save(commit=False)
            '''
            Se crea un token aleatorio, el cual se convertirá en el password provisional del usuario registrado
            '''
            activation_key = create_token()
            user.set_password(activation_key)
            '''
            Se le coloca como usuaio no activo con la finalidad de que al ingresar al sistema, la primera acción a realizar 
            sea cambiar su contraseña.
            '''
            user.is_active = 0
            user.save()
            user_pk = User.objects.get(id=user.id)
            role= post_values['rol']
            group= Group.objects.get(pk=role)
            user.groups.add(group)
            phone = post_values['phone']
            '''
            Se guardan los datos en la tabla uno a uno de la tabla user
            '''
            new_user = ProfileUser(fk_profileUser_user = user_pk, phone=phone, activationKey=activation_key)
            new_user.save()
            new_user_pk= ProfileUser.objects.get(id=new_user.pk)
            '''
            Se toman los proyectos asignados al usuario y se guardan en una lista, con la finalidad de verificar si
            existen o no en la base de datos. Si el proyecto no existe, se crea en la base de datos.
            '''
            proj1 = request.POST.get('project',None)
            proj2 = proj1.split(', ')
            for i in proj2:
                proj = Project.objects.filter(name=i).exists()
                if proj:
                    '''
                    Si el proyecto existe, se asocia el proyecto con el usuario. 
                    '''
                    proj_exist= Project.objects.get(name=i)
                    project_user = ProjectUser(project=proj_exist, user = new_user_pk)
                    project_user.save()
                else:
                    if i != '':
                        '''
                        En caso de que el proyecto n o exista, se crea y guarda en la base de datos y se asocia con el 
                        usuario.
                        '''
                        code = codeProject(i)
                        new_project = Project(code=code, name=i)
                        new_project.save()
                        proj_exist = Project.objects.get(name=i)
                        project_user = ProjectUser(project=proj_exist, user=new_user_pk)
                        project_user.save()

            '''
            Se envía un correo electrónico al usuario registrado en el sistema, con el username y password asignado.
            '''
            c = {'usuario': user.first_name,
                    'username':user.username,
                    'key': activation_key,
                    'host': request.META['HTTP_HOST']}

            email_subject = 'IDBC Group - Activación de cuenta'
            message_template = 'emailNewUser.html'
            email =[user.email]
            send_email(email_subject, message_template, c, email)

            messages.success(request, "El usuario ha sido guardado exitosamente")
            return HttpResponseRedirect(reverse_lazy('users'))
        else:
            messages.success(request, 'Error al registrar usuario')
            return render(request, 'page-new-user.html', {'form': form})

'''
Función que permite eliminar un usuario del sistema.
@:param: request: solicitud del sistema.
@:param: id: identificador del usaurio a ser eliminado.
'''
def DeleteUser(request,id):
    user = ProfileUser.objects.get(pk=id)
    user_pk = User.objects.get(pk=user.fk_profileUser_user.pk)
    task=Task.objects.filter(users=user).count()
    '''
    Si el usuario tiene asignado tareas, no se puede eliminar.
    '''
    if task > 0 :
        messages.success(request,"El usuario " + str(user.fk_profileUser_user.username) + " tiene tareas asociadas. No se puede eliminar")
        return HttpResponseRedirect(reverse_lazy('users'))
    user.delete()
    user_pk.delete()
    messages.success(request, "El usuario " + str(user.fk_profileUser_user.username) +" se ha eliminado exitosamente")
    return HttpResponseRedirect(reverse_lazy('users'))

'''
Función que permite el envío de correo electrónico a un usuario.
@:param subject: Asunto del email
@:param: message_template: Mensaje a enviar al usuario, viene dado por una plantilla HTML.
@:param context: Información que se quiera pasar al message_template.
@:param email: Dirección de correo electrónico al cual se le enviará el email.
'''
def send_email(subject, message_template, context, email):
    from_email = 'IDBC Group - Activación de cuenta'
    email_subject = subject
    message = get_template(message_template).render(context)
    msg = EmailMessage(email_subject, message, to=email, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()


'''
Función que permite generar un token aleatorio.
'''
def create_token():
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
    random.shuffle(chars)
    chars = ''.join(chars)
    sha1 = hashlib.sha1(chars.encode('utf8'))
    token = sha1.hexdigest()
    key = token[:12]
    return key

'''
Clase que permite verificar si es la primera sesión del usuario.
'''
class First_Session(TemplateView):
    template_name = 'first_session.html'

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = FirstSessionForm(post_values)
        if form.is_valid():
            activation_key = self.kwargs['activationKey']
            user = ProfileUser.objects.get(activationKey=activation_key)
            username = User.objects.get(pk = user.fk_profileUser_user.pk)
            password = post_values['password']
            password2 = post_values['password2']
            '''
            Si las contraseñas introducidas son iguales, el usuario pasa a ser activo y se guarda su nueva contraseña.
            '''
            if password == password2:
                username.set_password(password)
                username.is_active= 1
                username.save()
                form.add_error(None, 'La contraseña ha sido cambiada exitosamente')
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

'''
Clase que permite modificar un usuario.
'''
class Update_Users(TemplateView):
    template_name = 'page-new-user.html'
    form_class = UpdateUserForm

    def get_context_data(self, **kwargs):
        context = super(
            Update_Users, self).get_context_data(**kwargs)
        context['title'] = 'Modificar'
        user = ProfileUser.objects.get(pk=self.kwargs['id'])
        '''
        Se obtienen todos los proyectos asociados al usuario a modificar y se guardan en una lista.
        '''
        project_code = ProjectUser.objects.all().filter(user_id=user)
        x = []
        for i in project_code:
            proj = Project.objects.get(code=i)
            x.append(proj.name)
        '''
        Se le aplica join, con la finalidad de poder mostrarlos en la vista de modificar.
        '''
        proj_ass = ", ".join(x)

        '''
        Data que se muestra en la plantilla de modificar.
        '''
        data = {'first_name': user.fk_profileUser_user.first_name,
                 'last_name': user.fk_profileUser_user.last_name,
                 'username': user.fk_profileUser_user.username,
                 'rol': user.fk_profileUser_user.groups.all()[0],
                 'email' : user.fk_profileUser_user.email,
                'phone': user.phone,
                'project': proj_ass}
        form = UserForm(initial=data)
        context['userProfile'] = user
        context['project'] = proj_ass
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user_pk = self.kwargs['id']
            userProfile = ProfileUser.objects.get(pk=user_pk)
            user = User.objects.get(pk=userProfile.fk_profileUser_user.pk)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            userProfile.phone = request.POST['phone']
            user.username = request.POST['username']
            user.save()
            userProfile.save()
            role = request.POST['rol']
            group = Group.objects.get(pk=role)
            user.groups.remove(userProfile.fk_profileUser_user.groups.all()[0])
            user.groups.add(group)
            user.save()
            proj1 = request.POST.get('project', None)
            '''
            Si el campo de proyecto que se está recibiendo es vacío, es porque el usuario eliminó todos los proyectos
            asociados a él.
            '''
            if proj1 == '':
                oldProject = ProjectUser.objects.filter(user_id=userProfile)
                oldProject.delete()
            else:
                proj2 = proj1.split(', ')
                for i in proj2:

                    '''
                    Reviso los proyectos que introduce el usuario en el campo, si no existe se crea la instancia
                    '''
                    proj = Project.objects.filter(name=i).exists()
                    if proj:
                        proj_exist= Project.objects.get(name=i)
                        project_user=ProjectUser.objects.filter(user=user_pk, project=proj_exist.pk).exists()
                        '''
                        Si no existe la relación (usuario, proyecto) se asocia el proyecto con el usuario 
                        '''
                        if not project_user:
                            new_project_user = ProjectUser(user=userProfile, project=proj_exist)
                            new_project_user.save()
                    else:
                        if i != '':
                            '''
                            En caso de no existir el proyecto se crea su instancia y se asocia al usuario respectivo.
                            '''
                            code = codeProject(i)
                            new_project = Project(code=code, name=i)
                            new_project.save()
                            proj_exist = Project.objects.get(name=i)
                            project_user = ProjectUser(project=proj_exist, user=userProfile)
                            project_user.save()
                '''
                En caso de que se haya quitado una asociación de usuario con algún proyecto, se elimina dicha relación.
                '''
                allProject = ProjectUser.objects.filter(user_id=userProfile)
                for m in allProject:
                    count_exist = proj2.count(m.project.name)
                    if count_exist == 0:
                        p = Project.objects.get(code= m)
                        deleteProject = ProjectUser.objects.get(user_id = userProfile, project_id=p.code)
                        deleteProject.delete()

            messages.success(request, "El usuario ha sido modificado exitosamente")
            return HttpResponseRedirect(reverse_lazy('users'))
        else:
            return render(request, 'page-new-user.html',
                              {'form': form, 'pk': self.kwargs['id']})

'''
Clase que permite solicitar un cambio de contraseña.
'''
class Password_Reset(TemplateView):
    template_name = 'password-reset-form.html'
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = PasswordResetForm(post_values)
        if form.is_valid():
            email = post_values['email']
            user = User.objects.filter(email=email).exists()
            if user:
                username = User.objects.get(email = email)
                '''
                Si el usuario está activo, se procede a enviar un correo electrónico con la URL que lo llevará a restaurar
                su contraseña.
                '''
                if username.is_active:
                    user = ProfileUser.objects.get(fk_profileUser_user_id=username)
                    user.activationKey = create_token()
                    user.save()

                    c = {'usuario': username.first_name,
                        'username':username,
                        'key': user.activationKey,
                        'host': request.META['HTTP_HOST']
                    }

                    email_subject = 'IDBC Group - Recuperación de Contraseña'
                    message_template = 'password-reset-email.html'
                    email = [email]
                    send_email(email_subject, message_template, c, email)
                    return render(request, 'password-reset-done.html')
                else:
                    form.add_error(None, 'Lo sentimos, debe activar la cuenta')
                    return render(request, 'page-login.html',
                                  {'form': form})

            else :
                form.add_error(None, 'El correo ingresado no es válido, por favor verifique')
                return render(request, 'password-reset-form.html',
                              {'form': form})
        else:
            form.add_error(None, 'Ingrese un correo electrónico válido')
            return render(request,'password-reset-form.html',
                          {'form':form})


'''
Clase que permite cambiar cambiar una contraseña
'''
class Password_Reset_Confirm(TemplateView):
    template_name = 'password-reset-confirm.html'

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = FirstSessionForm(post_values)
        if form.is_valid():
            activation_key = self.kwargs['token']
            user = ProfileUser.objects.get(activationKey=activation_key)
            username = User.objects.get(pk=user.fk_profileUser_user.pk)
            password = post_values['password']
            password2 = post_values['password2']
            if password == password2:
                username.set_password(password)
                form.add_error(None, "Las contraseña se ha restablecido exitosamente.")
                return render(request, 'page-login.html', {'form':form})
            else:
                messages.success(request, 'Las contraseñas no coinceden, por favor verifique.')
                return HttpResponseRedirect(reverse_lazy('password_reset_confirm',
                                                         kwargs={'token': activation_key}))
        else:
            return render(request, 'password-reset-confirm.html', {'form':form, 'token':self.kwargs['token']})

'''
Clase que permite visualizar y modificar el perfil de un usaurio.
'''
class Profile(TemplateView):
    template_name = 'page-profile.html'
    form_class = UpdateProfileForm

    def get_context_data(self, **kwargs):
        context = super(
            Profile, self).get_context_data(**kwargs)

        user = ProfileUser.objects.get(fk_profileUser_user_id=self.kwargs['id'])
        data = {'first_name': user.fk_profileUser_user.first_name,
                 'last_name': user.fk_profileUser_user.last_name,
                 'username': user.fk_profileUser_user.username,
                 'rol': user.fk_profileUser_user.groups.all()[0],
                 'email' : user.fk_profileUser_user.email,
                'phone': user.phone,
                'imageProfile': user.imageProfile
                 }
        form = UserForm(initial=data)
        context['form'] = form
        context['users']=user
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_pk = kwargs['id']
            userProfile = ProfileUser.objects.get(fk_profileUser_user=user_pk)
            user = User.objects.get(pk=userProfile.fk_profileUser_user_id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            userProfile.phone = request.POST['phone']
            if (request.FILES == {}):
                pass
            else:
                userProfile.imageProfile = request.FILES['image_profile']
                userProfile.loadPhoto = True
            user.username = request.POST['username']
            user.save()
            userProfile.save()
            messages.success(request, "Su perfil ha sido actualizado exitosamente")
            return HttpResponseRedirect(reverse_lazy('profile',
                                                     kwargs={'id': user_pk}))
        else:
            return render(request, 'page-profile.html',
                          {'form': form})

'''
Función que permite crear el código del proyecto de manera aleatoria de acuerdo a las iniciales de su nombre.
@:param name: Nombre del proyecto al que se le va a crear un código.
'''
def codeProject(name):
    name = ''.join(name)
    return name[:3]

'''
Función que permite obtener los proyectos y son enviados mediante JSON a un JQuery. Esta función es utilizada para obtener
mediante Jquery el kwargs del proyecto.
'''
def get_projects(request):
    print("en get project")
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
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

'''
Función que permite validar si un email y/o un username existe en la base de datos
'''
def ValidateUser(request):
    email = request.POST.get('email', None)
    username = request.POST.get('username', None)
    data = {
        'email_exists': User.objects.filter(email=email).exists(),
        'username_exists': User.objects.filter(username=username).exists()
    }

    return JsonResponse(data)

