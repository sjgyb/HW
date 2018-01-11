#!/usr/bin/env python
import web
from web import form
import urllib2
import os
import sys, os, lucene
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

STORE_DIR1 = "index1"
STORE_DIR2 = "index2"

vm_env =lucene.initVM(vmargs=['-Djava.awt.headless=true'])
#base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
directory1 = SimpleFSDirectory(File(STORE_DIR1))
searcher1 = IndexSearcher(DirectoryReader.open(directory1))
directory2= SimpleFSDirectory(File(STORE_DIR2))
searcher2 = IndexSearcher(DirectoryReader.open(directory2))
analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
total_list=[]
