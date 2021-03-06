# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import admin

class Mobile(models.Model):
	PID = models.AutoField(primary_key=True, null=False, unique=True, default='')
	name = models.CharField(max_length=200, default='')
	code = models.CharField(max_length=20, default='')
	def __unicode__(self):
		return self.code
	'''class Meta:
		verbose_name = u"Mobile"'''

class Parameter(models.Model):
	p_PID = models.ForeignKey(Mobile, related_name='mobile_PID', on_delete=models.CASCADE)
	name = models.CharField(max_length = 20, default='')
	value = models.CharField(max_length = 200, default='')
	def __unicode__(self):
		return self.name
	'''class Meta:
		verbose_name = u"Parameter"

admin.site.register(Mobile)
admin.site.register(Parameter)'''
