# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User,Group
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

#User._meta.get_field('email')._unique = True

PHONE_VALIDATOR = RegexValidator(
    regex=r'^(0414|0412|0424|0416|0426)\d{7}$',
    message="Formato inválido.",
)

def get_name(self):
    return self.first_name + " " + self.last_name

User.add_to_class("__str__", get_name)


class ProfileUser(models.Model):
        fk_profileUser_user = models.OneToOneField(User, related_name='profile')
        phone = models.CharField(max_length=11, blank=True, validators=[PHONE_VALIDATOR])
        imageProfile = models.ImageField(upload_to='images/', blank=True)
        activationKey = models.CharField(max_length=40, blank=True)
        key_expires = models.DateTimeField(auto_now_add=True)
        loadPhoto = models.BooleanField(default=False)
        #project = models.ManyToManyField(Project)

        def __str__(self):
                return self.fk_profileUser_user.first_name + " " + self.fk_profileUser_user.last_name

