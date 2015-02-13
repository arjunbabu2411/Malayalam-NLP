#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication,QPushButton,QLineEdit,QFormLayout,QWidget,QTextEdit , QDesktopWidget
from collections import defaultdict
import math
import sys
try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)
class vml(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		document_filenames = {0 :"documents/mal1.txt",
							  1 :"documents/mal2.txt",
							  2 : "documents/mal3.txt"}
		N = len(document_filenames)
		print N
		dictionary = set()
		postings = defaultdict(dict)
		document_frequency = defaultdict(int)
		length = defaultdict(float)
		characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"
		####
		#self.initialize_terms_and_postings()
		#self.initialize_document_frequencies()
		#self. initialize_lengths()	
				
		self.resize(800,400)	# set size of window
		self.setFixedSize(self.size())
		self.entry  = QLineEdit(self)	# set object of QLineEdit()
		self.entry.resize(700,30)	#here we set size
		self.entry.setText(_translate("vml", "ഇവിടെ എഴുതുക", None))
		self.find = QPushButton("",self)
		self.find.setGeometry(700,0,100,30)
		self.find.setText(_translate("vml", "തിരയുക", None))
		self.connect(self.find,QtCore.SIGNAL("clicked()"),self.search)
		self.result = QTextEdit(self)
		self.result.setGeometry(4,34,792,362)
		
		
	def search(self):
		self.do_search()
			
	def initialize_terms_and_postings(self):

			
			for id in document_filenames:
				f = open(document_filenames[id],'r')
				document = f.read()
				f.close()
				terms = tokenize(document)
				unique_terms = set(terms)
				dictionary = dictionary.union(unique_terms)
				for term in unique_terms:
					postings[term][id] = terms.count(term)
	def tokenize(self,document):
		terms = document.lower().split()
		return [term.strip(characters) for term in terms]
	def initialize_document_frequencies():
		
		for term in dictionary:
			document_frequency[term] = len(postings[term])
	def initialize_lengths(self):
		
		for id in document_filenames:
			l = 0
			for term in dictionary:
				l += imp(term,id)**2
			length[id] = math.sqrt(l)
	def imp(term,id):
		if id in postings[term]:
			return postings[term][id]*inverse_document_frequency(term)
		else:
			return 0.0
	def inverse_document_frequency(self,term):
		if term in dictionary:
			return math.log(N/document_frequency[term],2)
		else:
			return 0.0
	def do_search(self):
		read_data = self.entry.text()
		#read_data = (read_data,"utf8")
		#entry_data = str(read_data)
		print read_data , entry_data
		
		#print query
		#if query == []:
			#sys.exit()
		relevant_document_ids = intersection(
				[set(postings[term].keys()) for term in query])
		print relevant_document_ids
		if not relevant_document_ids:
			print "No documents matched all query terms."
		else:
			scores = sorted([(id,similarity(query,id))
							 for id in relevant_document_ids],
							 key=lambda x: x[1],
							 reverse=True)
			print "Score: filename"
			for (id,score) in scores:
				print str(score)+": "+document_filenames[id]
			filename = document_filenames[id] 
			f = open(filename, 'r')
			filedata = f.read()
			self.result.setText(filedata)
			f.close()
	def intersection(self,sets):
		return reduce(set.intersection, [s for s in sets])
	def similarity(self,query,id):
		similarity = 0.0
		for term in query:
			if term in dictionary:
				similarity += inverse_document_frequency(term)*imp(term,id)
		similarity = similarity / length[id]
		return similarity
		
app_object = QApplication(sys.argv)
vml_obj = vml()
vml_obj.show()
sys.exit(app_object.exec_())

		
		
		
