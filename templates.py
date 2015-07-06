#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: templates.py: javascript functions for Medilab Web App
# By: Anass Ahmed

"""
a lot of javascript functions that control the Templates Pages Appearance.
"""

import datetime
from templates_db import *
from okasha.baseWebApp import *
from functions import *

def viewTemplatesPage(script_s, query):
    
    """ A small function shows the main Templates page """
    
    return """\
    $.get("%(script)s/templates/?%(query)s", function(data) {
        $("#content").html(data).show("fast");
	}); """ %{'script':script_s, 'query':query}

def viewMainTemplatesPage(script_s):
    
    """ A small function shows the main Templates Page """
    
    return """\
    $("#templatesPage").show("fast"); 
    %(templatesList)s
    $("#searchBtn").click(function() {
        $("#templatesList").hide("fast");
        $("#viewTemplatesResults").hide("fast").html("");
        var term = document.searchForm.term.value;
        $.get("%(script)s/templates/", {view: "search", term: term}, function(data) {
            $("#templatesList").hide("fast");
            $("#viewTemplatesResults").html(data).show("fast");
        });
    });""" %{'templatesList':viewTemplatesList(script_s), 'script':script_s}

def viewTemplateElement(id, title, fromAge, toAge, price, script_s):
    
    """ A function shows the important information for a Template as a row in a table """
    
    return """\
    <tr><td class="center-text"><span>%(id)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/templates?view=template&id=%(id)s"><span>%(title)s</span></a></td>\
    <td class="center-text"><span>%(fromAge)s</span></td>\
    <td class="center-text"><span>%(toAge)s</span></td>\
    <td class="center-text"><span>%(price)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/templates?view=edit&id=%(id)s" class="non-borders"><button>Edit</button></a></td>\
    <td class="center-text"><a href="%(script)s/page/templates?process=delete&id=%(id)s" class="non-borders"><button>Delete</button></a></td></tr> """ %{'id':id, 'title':title, 'fromAge':fromAge, 'toAge':toAge, 'price':price, 'script':script_s}
    
def viewTemplatesList(script_s):
    
    """ A function shows all Templates in the DB in a table """
    
    templatesList = """\
    <tr>\
    <th>ID</th>\
    <th>Title</th>\
    <th>From Age</th>\
    <th>To Age</th>\
    <th>Price</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr>\ """
    
    setup_all()
    
    for i in templates.query.all():
        templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
    return """\
    $("#templatesListTable").html('%s').show("fast");
    $("#templatesList").show("fast"); """ %templatesList 

def processTemplatesResults(term, script_s):
    
    """ A function shows the Search Results in Templates Page """
    
    templatesList = """\
    <tr>\
    <th>ID</th>\
    <th>Title</th>\
    <th>From Age</th>\
    <th>To Age</th>\
    <th>Price</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr>\ """
    
    for i in templates.query.all():
        try:
            if term.startswith("from_age: "):
                if i.from_age == int(term[10:]):
                    templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
            elif term.startswith("to_age: "):
                if i.to_age == int(term[8:]):
                    templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
            elif term.startswith("price: "):
                if i.price == float(term[7:]):
                    templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
            elif i.id == int(term):
                templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
        except ValueError: pass
        if i.title.startswith(term):
            templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
        elif i.title.endswith(term):
            templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
        elif i.title.find(term) != -1:
            templatesList += viewTemplateElement(id=i.id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
    return """\
    $("#templatesResultsAjaxTable").html('%s').show("fast");
    $("#templatesResultsAjax").show("fast"); """ %templatesList 

def viewAddTemplate(script_s):
    
    """ A function shows the Add Template Form and sends data to Templates Page """
    
    return """\
    document.addTemplate.process.value = "add";
    document.addTemplate.id.value = "";
    $("div#addTemplate").show("fast");
    $("#backToTemplate").hide("fast");
    $("input[type=button]#submit").click(function() {
        var title = document.addTemplate.title.value;
        var fromAge = document.addTemplate.fromAge.value;
        var toAge = document.addTemplate.toAge.value;
        var price = document.addTemplate.price.value;
        contentInput.removeInstance('content_input');
        var content = document.addTemplate.content_input.value;
        var notes = document.addTemplate.notes.value;
        $.post("%(script)s/templates/", {
        process: "add",
        id: "",
        title: title,
        fromAge: fromAge,
        toAge: toAge,
        price: price,
        content: content,
        notes: notes
        }, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'script':script_s}

def viewEditTemplate(id, script_s):
    
    """ A function shows the Edit Template form and sends data to Template Page """
    
    setup_all()
    template = templates.get_by(id = id)
    title = template.title
    fromAge = template.from_age
    toAge = template.to_age
    price = template.price
    content = template.content
    notes = template.notes
    
    content = filter_js_lines(filter_single_quotes(content))
    
    notes = filter_js_lines(filter_single_quotes(notes))
    
    return """\
    $("div#addTemplate h1").html("Edit Template");
    document.addTemplate.submit.value = "Edit Template";
    document.addTemplate.title.value = "%(title)s";
    document.addTemplate.fromAge.value = %(fromAge)s;
    document.addTemplate.toAge.value = %(toAge)s;
    document.addTemplate.price.value = %(price)s;
    $("#notes").html('%(notes)s');
    $("#content_input").text('%(content)s');
    document.getElementById("backToTemplate").href += "%(id)s";
    $("div#addTemplate").show("fast");
    $("input[type=button]#submit").click(function() {
        var title = document.addTemplate.title.value;
        var fromAge = document.addTemplate.fromAge.value;
        var toAge = document.addTemplate.toAge.value;
        var price = document.addTemplate.price.value;
        contentInput.removeInstance('content_input');
        var content = document.addTemplate.content_input.value;
        var notes = document.addTemplate.notes.value;
        $.post("%(script)s/templates/", {
        process: "edit",
        id: %(id)s,
        title: title,
        fromAge: fromAge,
        toAge: toAge,
        price: price,
        content: content,
        notes: notes
        }, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'id':id, 'title':title, 'fromAge':fromAge, 'toAge':toAge, 'price':price, 'content':content, 'notes':notes, 'script':script_s}

def viewTemplate(id, script_s):
    
    """ A function show the Template Information in a Table """
    
    setup_all()
    template = templates.get_by(id = id)
    title = template.title
    fromAge = template.from_age
    toAge = template.to_age
    price = template.price
    content = template.content
    notes = template.notes
    
    content_nolines = content.splitlines()
    content = filter_single_quotes("".join(content_nolines))
    
    notes = filter_html_lines(filter_single_quotes(notes))
    
    return """\
    $("#view_id").html("%(id)s");
    $("#view_title").html("%(title)s");
    $("#view_fromAge").html("%(fromAge)s");
    $("#view_toAge").html("%(toAge)s");
    $("#view_price").html("%(price)s");
    $("#view_content").html('%(content)s');
    $("#view_notes").html('%(notes)s');
    document.getElementById("editBtn").href += "%(id)s";
    $("#viewTemplate").show("fast"); 
    $("#deleteBtn").click(function() {
        s = confirm("Are You Sure You Want to Delete this Template? ")
        if (s) {
            $.post("%(script)s/templates/", {process: "delete", id: "%(id)s"}, function(data) {
                $("#content").html(data).show("fast");
            });
        };
    });""" %{'id':id, 'title':title, 'fromAge':fromAge, 'toAge':toAge, 'price':price, 'content':content, 'notes':notes, 'script':script_s}

def viewDeletedTemplate(id):
    
    """ Small function that shows small message tells you that the Template was deleted Successfully """
    
    setup_all()
    template = templates.get_by(id = id)
    template.delete()
    session.commit()
    
    return """\
    $("#deleted").show("fast"); """
