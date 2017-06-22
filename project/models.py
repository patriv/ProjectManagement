# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User,Group
from django.db import models

# Create your models here.

class profileUser(models.Model):
        user = models.OneToOneField(User)
        role = models.ForeignKey(Group)
        phone = models.CharField(max_length=11, blank=True)
        image_profile = models.ImageField(upload_to='images/', blank=True)

        def __str__(self):
                return self.user.first_name + "" + self.user.last_name
