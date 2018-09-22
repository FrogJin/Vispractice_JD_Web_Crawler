# -*- coding: utf-8 -*-
import os.path, shutil
from whoosh import writing
from whoosh.index import create_in, open_dir
from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.query import *
from whoosh.qparser import QueryParser

# Get the index; Return an index
def get_index():
	ix = ''
	if not os.path.exists("index"):
		os.mkdir("index")
		schema = Schema(PID = NUMERIC(unique = True),\
					name = TEXT(stored = True),\
					code = TEXT(stored = True),\
					parameter = TEXT(stored = True))
		ix = create_in("index", schema)
	else: ix = open_dir("index")
	return ix

# Get the writer of the index; Return a index writer
def get_writer_of_index(ix):
	writer = ix.writer()
	#writer.mergetype = writing.CLEAR	# Rebuild the index
	return writer

# Add a document to writer
def add_document_to_writer(writer, p_PID, p_name, p_code, p_parameter):
	writer.add_document(PID=u"{PID}".format(PID=p_PID), name=u"{name}".format(name=p_name), code=u"{code}".format(code=p_code), parameter=u"{para}".format(para=p_parameter))

# Update an existed document of the writer
def update_document_of_writer(writer, p_PID, p_name, p_code, p_parameter):
	writer.update_document(PID=u"{PID}".format(PID=p_PID), name=u"{name}".format(name=p_name), code=u"{code}".format(code=p_code), parameter=u"{para}".format(para=p_parameter))

# Drop the index
def drop_index():
	shutil.rmtree("index")

# Commit writer
def commit_writer(writer):
	writer.commit(optimize = True)		# Auto optimize the index

