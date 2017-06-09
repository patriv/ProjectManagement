# -*- coding: utf-8 -*-
from django.views.generic import *
from django.shortcuts import render

class Login(TemplateView):
    template_name = 'page-login.html'

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
