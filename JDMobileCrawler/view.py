# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
#from JDMobile.models import JDMobile
import MySQLdb

def hello(request):
	context = {}
	context['hello'] = 'Hello World! '
	return render(request, 'hello.html', context)
	#return HttpResponse("Hello world !")
