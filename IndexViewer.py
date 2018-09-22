# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from whoosh.index import open_dir
from whoosh.query import Every

ix = open_dir("index")
print ix.schema			# Print the schema of the index

results = ix.searcher().search(Every('code'))
for result in results:
	print "code: {code}, name: {name}, parameter: {parameter}".format(code = result["code"], name = result["name"], parameter = result["parameter"])	# Print everything in the index
