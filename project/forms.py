#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from project.models import profileUser
from django.db import models
from role.forms import *


class LoginForm(forms.Form):
	class Meta:
		model = User
		fields = ('username','password','email',)

class UserForm(forms.ModelForm):
	first_name = forms.CharField()
	last_name= forms.CharField()
	username=forms.CharField()
	phone = forms.CharField(required=False)
	email = forms.EmailField()
	group=Group.objects.all()
	new=[]
	for i in group:
		new.append((i.id,i.name))

	rol = forms.ChoiceField(
        required=True,
        choices=new
    )

	print(new)
	class Meta:
		model= User
		fields = ('first_name','last_name','username','email')
