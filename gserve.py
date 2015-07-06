#! /usr/bin/python
# -*- coding: UTF-8 -*-
import sys, os, os.path
from main import MediLab
 
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
 
d=os.path.dirname(__file__)
#application=webApp(os.path.join(d, 'templates'),staticBaseDir={'/_files/':os.path.join(d, 'files')});
application=MediLab(
      'SafeMode',
      os.path.join(d,'templates'),
      staticBaseDir={'/files/':os.path.join(d,'files')}
    );
run_wsgi_app(application)
