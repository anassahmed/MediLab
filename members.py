#_*_ coding: UTF8 _*_
#!/usr/bin/python
# Filename: members.py: JS functions controls Members Pages Appearance.

from db import *
from functions import *
import hashlib

def viewMembersPage(script_s, query):
    
    """ A small Function shows the main page of members """
    
    return """\
    $.get("%(script)s/members/?%(query)s", function(data) {
        $("#content").html(data).show("fast");
    });""" %{'script':script_s, 'query':query}
    
def viewMainMembersPage(script_s):
    
    """ A function shows the main page of members """
    
    return """\
    $("#membersListTable").html('%s');
    $("#membersPage").show("fast");
    $("#membersList").show("fast");""" %viewMembersList(script_s)

def viewMemberElement(id, script_s):
    
    """ A Function shows a member information as a table row """
    
    setup_all()
    member = members.get_by(id = id)
    
    is_admin = "Members"
    if member.is_admin: is_admin = "Administrators"
    
    is_banned = "No"
    if member.is_banned: is_banned = "Yes"
    
    return """\
    <tr>\
    <td class="center-text"><span>%(id)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/members/?view=member&id=%(id)s"><span>%(username)s</span></td>\
    <td class="center-text"><span>%(email)s</span></td>\
    <td class="center-text"><span>%(phone)s</span></td>\
    <td class="center-text"><span>%(is_admin)s</span></td>\
    <td class="center-text"><span>%(is_banned)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/members/?view=edit&id=%(id)s" class="non-borders"><button>Edit</button></a></td>\
    <td class="center-text"><a href="%(script)s/page/members/?process=delete&id=%(id)s" class="non-borders"><button>Delete</button></a></td>\
    </tr>""" %{'id': member.id, 'username':member.username, 'email':member.email, 'phone':member.phone, 'is_admin':is_admin, 'is_banned':is_banned, 'script':script_s}

def viewMembersList(script_s):
    
    """ A function shows All Members in One List """
    
    membersList = """\
    <tr>\
    <th>ID</th>\
    <th>Username</th>\
    <th>Email</th>\
    <th>Phone</th>\
    <th>Group</th>\
    <th>Banned?</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    </tr> """
    
    setup_all()
    for i in members.query.all():
        membersList += viewMemberElement(i.id, script_s)
    
    return membersList

def viewMember(id):
    
    """ A function shows the Member's Information """
    
    setup_all()
    member = members.get_by(id = id)
    
    is_admin = "Members"
    if member.is_admin: is_admin = "Administrators"
    
    is_banned = "No"
    if member.is_banned: is_banned = "Yes"
    
    ban_reason = ""
    if member.ban_reason != None: ban_reason = filter_html_lines(filter_single_quotes(member.ban_reason))
    
    return """\
    $("#view_username").html("%(username)s");
    $("#view_email").html("%(email)s");
    $("#view_phone").html("%(phone)s");
    $("#view_is_admin").html("%(is_admin)s");
    $("#view_is_banned").html("%(is_banned)s");
    $("#view_ban_reason").html('%(ban_reason)s');
    document.getElementById("editBtn").href += %(id)s;
    document.getElementById("deleteBtn").href += %(id)s;
    $("#viewMember").show("fast"); """ %{'id':member.id, 'username':member.username, 'email':member.email, 'phone':member.phone, 'is_admin':is_admin, 'is_banned':is_banned, 'ban_reason':ban_reason}

def viewAddMember(script_s):
    
    """ A function shows the Add Member Form """
    
    return """\
    $(".editOnly").hide();
    $("#backToMember").hide();
    $("#addMember").show("fast"); 
    $("#submit").click(function() {
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;
        var phone = document.getElementById('phone').value;
        var is_admin = document.getElementById('is_admin').value;
        $.post("%(script)s/members/", {
        process: "add",
        username: username,
        password: password,
        email: email,
        phone: phone,
        is_admin: is_admin}, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'script':script_s}

def viewEditMember(id, script_s):
    
    """ A function shows the Add Member Form and Edit it """
    
    setup_all()
    
    member = members.get_by(id = id)
    
    is_banned = "false"
    if member.is_banned: is_banned = "true"
    
    ban_reason = ""
    if member.ban_reason != None: ban_reason = filter_js_lines(filter_single_quotes(member.ban_reason))
    
    return """\
    document.getElementById('username').value = "%(username)s";
    document.getElementById('email').value = "%(email)s";
    document.getElementById('phone').value = "%(phone)s";
    document.getElementById('is_admin').value = %(is_admin)s;
    document.getElementById("is_banned").checked = %(is_banned)s;
    $("#ban_reason").text('%(ban_reason)s');
    $("#addMember h1").html("Edit Member");
    document.getElementById("submit").value = "Edit Member";
    document.getElementById("backToMember").value += "%(id)s";
    $("#addMember").show("fast"); 
    $("#submit").click(function() {
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;
        var phone = document.getElementById('phone').value;
        var is_admin = document.getElementById('is_admin').value;
        is_banned = 0;
        if (document.getElementById("is_banned").checked) {
            var is_banned = 1;
        };
        ban_reason = document.getElementById('ban_reason').value;
        $.post("%(script)s/members/", {
        process: "edit",
        id: %(id)s,
        username: username,
        password: password,
        email: email,
        phone: phone,
        is_admin: is_admin,
        is_banned: is_banned,
        ban_reason: ban_reason}, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'script':script_s, 'id': member.id, 'username':member.username, 'email':member.email, 'phone':member.phone, 'is_admin':member.is_admin, 'is_banned':is_banned, 'ban_reason':ban_reason}

def viewDeletedMember(id, script_s):
    
    """ show A deleted Message """
    
    setup_all()
    
    member = members.get_by(id = id)
    member.delete()
    
    return "window.location.replace('%(script)s/page/members/?view=deleted" %{'script':script_s}
