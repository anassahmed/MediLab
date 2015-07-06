#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: customers.py: javascript functions for Medilab Web App
# By: Anass Ahmed

"""
a lot of javascript functions that control the Customers Pages Appearance.
"""

import datetime
from db import *
from okasha.baseWebApp import *
from bills import *
from functions import *

def viewCustomersPage(script_s, query):
    
    """ A small function that shows the Customers Page """ 
    
    return """\
    $.get("%(script)s/customers/?%(query)s", function(data) {
        $("#content").html(data).show("fast");
    }); """ %{'script': script_s, 'query':query}
    
def viewCustomerElement(id, name, birth, gender, billsNum, rebortsNum, script_s):
    
    """ A function shows a Customer's Information in a Table """
    
    now = datetime.date.today()
    age = now.year - birth.year
    
    return """\
    <tr><td class="center-text"><span>%(id)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/customers?view=customer&id=%(id)s"><span>%(name)s</span></a></td>\
    <td class="center-text"><span>%(age)s</span></td>\
    <td class="center-text"><span>%(birth)s</span></td>\
    <td class="center-text"><span>%(gender)s</span></td>\
    <td class="center-text"><span>%(billsNum)s</span></td>\
    <td class="center-text"><span>%(rebortsNum)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/customers?view=edit&id=%(id)s" class="non-borders"><button>Edit</button></a></td>\
    <td class="center-text"><a href="%(script)s/page/customers?process=delete&id=%(id)s" class="non-borders"><button>Delete</button></a></tr>\
    """ %{'id':id, 'name':name, 'age':age, 'birth':birth, 'gender':gender, 'billsNum':billsNum, 'rebortsNum':rebortsNum, 'script':script_s}
    
def viewCustomersList(script_s):
    
    """ A function shows All Cutomers in a table """
    
    setup_all()
    CustomersList = """\
    <tr>\
    <th>ID</th>\
    <th>Name</th>\
    <th>Age</th>\
    <th>Birth Date</th>\
    <th>Gender</th>\
    <th>Bills Number</th>\
    <th>Reports Number</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    </tr>"""
    for i in customers.query.all():
        CustomersList += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
    return CustomersList

def processCustomersResults(term, script_s):
    
    """ A function searches in the Customers DB to get results """
    
    setup_all()
    CustomersList = """\
    <tr>\
    <th>ID</th>\
    <th>Name</th>\
    <th>Age</th>\
    <th>Birth Date</th>\
    <th>Gender</th>\
    <th>Bills Number</th>\
    <th>Reports Number</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    </tr>"""
    firstResults = ""
    secondResults = ""
    for i in customers.query.all():
        try:
            if term.startswith("age: "):
                now = datetime.date.today()
                age = now.year - i.birth.year
                if age==int(term[5:]):
                    firstResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        except ValueError: pass
        if term.startswith("gender: "):
            if i.gender==term[8:]:
                firstResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        elif term.startswith("birth: "):
            if i.birth.strftime("%Y-%m-%d")==term[7:]:
                firstResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        elif i.name.startswith(term):
            firstResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        elif i.name.endswith(term):
            secondResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        elif i.name.find(term) != -1:
            secondResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        try:
            if i.id == int(term):
                firstResults += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), script_s)
        except ValueError: pass
    CustomersList += firstResults + secondResults
    return CustomersList 

def viewCustomersResults(term, script_s):
    return """\
    $("div#customersResultsAjax").show("fast");
    $("#customersResultsTableAjax").html('%s').show("fast"); """ %processCustomersResults(term, script_s)

def viewMainCustomersPage(script_s):
    
    """ function show the Main Page of Customers Pages """
    
    mainPage = """\
    $("#customersPage").show("fast");
    $("#customersList").show("fast");
    $("#customersListTable").html('%s').show("fast");
    $("#searchBtn").click(function() {
        $("#customersList").hide("fast");
        $("#customersResultsTable").html('').hide("fast");
        $("#customersResults").show("fast");
        term = document.customersSearch.term.value;
        $.get("%s/customers/", {view: "search", term: term}, function(data) {
            $("#customersResultsTable").html(data).show("fast");
        });
    }); """ %(viewCustomersList(script_s), script_s)
    return mainPage

def viewAddCustomer(script_s):
    
    """ Function shows the Add Customer Form """
    
    return """\
    document.addCustomer.process.value = "add";
    document.addCustomer.id.value = "";
    $("div#addCustomer").show("fast"); 
    $("#backToDetails").hide("fast");
    $("#submit").click(function () {
        var process = "add";
        var name = document.addCustomer.name.value;
        var birth_d = document.addCustomer.birth_d.value;
        var birth_m = document.addCustomer.birth_m.value;
        var birth_y = document.addCustomer.birth_y.value;
        var gender = document.addCustomer.gender.value;
        var phone = document.addCustomer.phone.value;
        var address = document.addCustomer.address.value;
        var notes = document.addCustomer.notes.value;
        $.post("%(script)s/customers/", {
        process: process,
        name: name,
        birth_d: birth_d,
        birth_m: birth_m,
        birth_y: birth_y,
        gender: gender,
        phone: phone,
        address: address,
        notes: notes
        }, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'script': script_s}

def viewEditCustomer(id, script_s):
    
    """ A function modifies the Add Form to be the Edit Customer Form """
    
    setup_all()
    customer = customers.get_by(id = id)
    
    name = customer.name
    birth = customer.birth
    gender = customer.gender
    phone = customer.phone
    address = customer.address
    notes = customer.notes
    
    birth_d = birth.day
    birth_m = birth.month
    birth_y = birth.year
    
    address = filter_js_lines(filter_single_quotes(address))
    notes = filter_js_lines(filter_single_quotes(notes))
    
    return """\
    document.addCustomer.process.value = "edit";
    document.addCustomer.id.value = %(id)s;
    document.addCustomer.name.value = "%(name)s";
    document.addCustomer.birth_d.value = "%(birth_d)s";
    document.addCustomer.birth_m.value = "%(birth_m)s";
    document.addCustomer.birth_y.value = "%(birth_y)s";
    document.addCustomer.gender.value = "%(gender)s";
    document.addCustomer.phone.value = "%(phone)s";
    document.addCustomer.submit.value = "Edit Customer";
    $("div#addCustomer h1").html("Edit Customer").show("fast");
    $("#address").text("%(address)s");
    $("#notes").text("%(notes)s");
    $("div#addCustomer").show("fast"); 
    document.getElementById("backToDetailsLink").href += "%(id)s";
    $("#backToDetails").show("fast");
    $("#submit").click(function () {
        var process = "edit";
        var id = %(id)s;
        var name = document.addCustomer.name.value;
        var birth_d = document.addCustomer.birth_d.value;
        var birth_m = document.addCustomer.birth_m.value;
        var birth_y = document.addCustomer.birth_y.value;
        var gender = document.addCustomer.gender.value;
        var phone = document.addCustomer.phone.value;
        var address = document.addCustomer.address.value;
        var notes = document.addCustomer.notes.value;
        $.post("%(script)s/customers/", {
        process: process,
        id: id,
        name: name,
        birth_d: birth_d,
        birth_m: birth_m,
        birth_y: birth_y,
        gender: gender,
        phone: phone,
        address: address,
        notes: notes,
        }, function(data) {
            $("#content").html(data).show("fast");
        });
    });
    """ %{'name':name, 'birth_d':birth_d, 'birth_m':birth_m, 'birth_y':birth_y, 'gender':gender, 'phone':phone, 'address':address, 'notes':notes, 'id': id, 'script': script_s}

def viewCustomer(id, script_s):
    
    """ A function shows a Customer information in a table """
    
    setup_all()
    customer = customers.get_by(id = id)
    name = customer.name
    birth = customer.birth
    gender = customer.gender
    phone = customer.phone
    address = customer.address
    notes = customer.notes
    
    now = datetime.date.today()
    age = now.year - birth.year
    address = filter_html_lines(filter_single_quotes(address))
    notes = filter_html_lines(filter_single_quotes(notes))
    
    return """\
    $("#view_id").html(%(id)s);
    $("#view_name").html("%(name)s");
    $("#view_birth").html("%(birth)s");
    $("#view_age").html("%(age)s");
    $("#view_gender").html("%(gender)s");
    $("#view_phone").html("%(phone)s");
    $("#view_address").html("%(address)s");
    $("#view_notes").html("%(notes)s");
    document.getElementById("addBillBtn").href += "%(id)s";
    $("div#viewCustomer").show("fast"); 
    $("#edit").click(function() {
        $.get("%(script)s/customers/", {view: "edit", id: %(id)s}, function(data) {
            $("#content").html(data).show("fast");
        });
    });
    $("#delete").click(function() {
        deleteQ = confirm("Are You Sure that you want to delete this customer?")
        if (deleteQ)
        {
            $.get("%(script)s/customers/", {process: "delete", id: %(id)s}, function(data) {
                $("#content").html(data).show("fast");
            });
        }
    });
    %(billsList)s """ %{'id':id, 'name':name, 'birth':birth, 'gender':gender, 'phone':phone, 'address':address, 'notes':notes, 'script':script_s, 'age':age, 'billsList':viewCustomerBillsList(id, script_s)}

def viewDeletedCustomer(id):
    
    """ Small function that shows small message tells you that the Customer was deleted Successfully """
    
    setup_all()
    customer = customers.get_by(id = id)
    if customer == None: raise fileNotFoundException()
    for i in customer.reports:
        if i != None:
            i.delete()
    for i in customer.bills:
        if i != None:
            i.delete()
    customer.delete()
    session.commit()
    
    return """\
    $("#deleted").show("fast"); """
