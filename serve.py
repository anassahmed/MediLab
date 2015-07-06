#_*_ coding: UTF-8 _*_
#!/usr/bin/python
"""
Serving the Web App by Paste.HTTPServer to the browser.
"""

from paste import httpserver
from main import MediLab
import os, os.path, sys
import logging

d = os.path.dirname(sys.argv[0])

app = MediLab(os.path.join(d, "templates"), staticBaseDir={'/files/':os.path.join(d, "files")});
httpserver.serve(app, host = "127.0.0.1", port = 8082)
