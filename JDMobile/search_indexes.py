from haystack import indexes
from models import Mobile, Parameter

class MobileIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	name = indexes.CharField(model_attr='name')
	code = indexes.CharField(model_attr='code')

	def get_model(self):
		return Mobile

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

class ParameterIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document = True, use_template = True)
	name = indexes.CharField(model_attr='name')
	value = indexes.CharField(model_attr='value')
	p_PID = indexes.CharField(model_attr='p_PID')

	def get_model(self):
		return Parameter

	def index_queryset(self, using=None):
		return self.get_model().objects.all()
