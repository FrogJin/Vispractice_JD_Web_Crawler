# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Mobile, Parameter
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import MultifieldParser
from haystack.forms import SearchForm

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MobileSearchForm(SearchForm):
	def no_query_found(self):
		return self.searchqueryset.all()
	def search(self):
		sqs = super(MobileSearchForm,self).search().models(Mobile)
		if not self.is_valid():
			return self.no_query_found()
		return sqs

class ParameterSearchForm(SearchForm):
	def no_query_found(self):
		return self.searchqueryset.all()
	def search(self):
		sqs = super(ParameterSearchForm,self).search().models(Parameter)
		if not self.is_valid():
			return self.no_query_found()
		return sqs

def search(request):
	results = []
	if request.GET.get('q', ''):
		mobile_results = MobileSearchForm(request.GET).search()
		parameter_results = ParameterSearchForm(request.GET).search()
		for mobile in mobile_results:
			results.append(mobile.object)
		for parameter in parameter_results:
			p_PID = parameter.object.p_PID_id
			mobile = Mobile.objects.get(PID=p_PID)
			if mobile not in results:
				results.append(mobile)	
	return render(request, 'search.html', {'results': results})

def detail(request, mobile_code):
	mobile = Mobile.objects.get(code=mobile_code)
	parameters = Parameter.objects.filter(p_PID_id=mobile.PID)
	return render(request, 'mobile_details.html', {'mobile': mobile, 'parameters': parameters})
