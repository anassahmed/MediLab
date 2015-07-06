#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: JSFunctions.py: javascript functions for Medilab Web App
# By: Anass Ahmed

from db import *
import datetime, time


def viewMainPage(script_s):
    
    """ A small function that shows the Main Page """
    
    return """\
    $.get("%(script)s/main/", function(data) {
        $("#content").html(data).show("fast");
    }); """ %{'script': script_s}

def viewAboutPage(script_s):
    
    """ A small function that shows the About Page """
    
    return """\
    $.get("%(script)s/about/", function(data) {
        $("#content").html(data).show("fast");
    }); """ %{'script': script_s}

def the_editor(script_s):
    
    """ Small function to Call the Editor """
    
    return """\
<script type="text/javascript" src="%(script)s/files/nicEdit.js"></script>
<textarea></textarea>
<script type="text/javascript">
	bkLib.onDomLoaded(function() { nicEditors.allTextAreas() });
</script>
 """ %{'script':script_s}

def filter_html_lines(text):
    
    """ replace lines with HTML lines """
    
    if text == None: text = "None"
    text_nolines = text.splitlines()
    text = "<br />".join(text_nolines)
    return text

def filter_js_lines(text):
    
    """ replace lines with javascript lines """
    
    if text == None: text = "None"
    text_nolines = text.splitlines()
    text = "\\n".join(text_nolines)
    return text

def filter_single_quotes(text):
    
    """ add back slash before single quotes """
    
    text_noquotes = text.replace("'","\\'")
    return text_noquotes

def userLoggedin(rq):
    
    """ validate if user logged in -> return True if logged or False if not logged """
    
    setup_all()
    if not rq.cookies.has_key('medilab_session'): return False
    login_session = sessions.get_by(session_hash = rq.cookies['medilab_session'].value.decode('utf8'))
    if login_session == None: return False
    else: return True

def whoIsLogged(rq):
    
    """ return the member who is Logged in """
    
    setup_all()
    login_session = sessions.get_by(session_hash = rq.cookies['medilab_session'].value.decode('utf8'))
    member = members.get_by(username = login_session.username)
    
    return member

def userLoggedisAdmin(rq):
    
    """ returns that the member is administrator or No """
    
    setup_all()
    login_session = sessions.get_by(session_hash = rq.cookies['medilab_session'].value.decode('utf8'))
    member = members.get_by(username = login_session.username)
    
    if member.is_admin: return True
    else: return False
