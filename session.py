#_*_ coding: UTF8 _*_
#!/usr/bin/python
# Filename: session.py: JS functions controls Session Pages Appearance.

from db import *
from functions import *

def viewUserError():
    
    """ A small function shows an error message tells you that the Username is not found """
    
    return """\
    $("#loginUserError").show("fast"); """
    
def viewPassError():
    
    """ A Small function shows an error message tells you that the password is not correct """
    
    return """\
    $("#loginPassError").show("fast"); """
    
def viewLoggedOut():
    
    """ A small function shows a message tells you that you logged out successfully """
    
    return """\
    $("#logoutSuccess").show("fast"); """

def addReturnUrl(url):
    
    """ add rerturn url in the login form """
    
    return """\
    document.getElementById("returnUrl").value = "%(url)s"; """ %{'url':url}
    
def viewBanError(id):
    
    """ A small function shows the ban reason for the banned member """
    
    setup_all()
    member = members.get_by(id = id)
    ban_reason = filter_js_lines(filter_single_quotes(member.ban_reason))
    
    return """\
    $("#ban_reason").html('%s');
    $("#banError").show("fast"); """ %ban_reason

