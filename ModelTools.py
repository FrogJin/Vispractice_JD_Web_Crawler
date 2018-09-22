# -*- coding: utf-8 -*-
from JDMobile.models import Mobile, Parameter

def add_mobile(p_name, p_code):
	Mobile.objects.create(name = p_name, code = p_code)

def update_mobile(p_name, p_code):
	Mobile.objects.filter(code = p_code).update(name = p_name)

def add_parameter(pa_name, pa_value, p_PID):
	Parameter.objects.create(name = pa_name, value = pa_value, PID = p_PID)

def update_parameter(pa_name, pa_value, p_PID):
	Parameter.objects.filter(name = pa_name, PID = p_PID).update(value = pa_value)
