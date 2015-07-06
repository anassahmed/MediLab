#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: reports.py: javascript functions for Medilab Web App
# By: Anass Ahmed

"""
a lot of javascript functions that control the Reports Pages Appearance.
"""

import datetime
from db import *
from okasha.baseWebApp import *
from functions import *

def viewReportsPage(script_s, query):
    
    """ A small function shows the main Reports page """
    
    return """\
    $.get("%(script)s/reports/?%(query)s", function(data) {
        $("#content").html(data).show("fast");
	}); """ %{'script':script_s, 'query':query}

def viewMainReportsPage(script_s):
    
    """ A small function shows the main Reports Page """
    
    return """\
    $("#reportsPage").show("fast"); 
    %(reportsList)s
    $("#searchBtn").click(function() {
        $("#reportsList").hide("fast");
        $("#viewReportsResults").hide("fast").html("");
        var term = document.searchForm.term.value;
        $.get("%(script)s/reports/", {view: "search", term: term}, function(data) {
            $("#reportsList").hide("fast");
            $("#viewReportsResults").html(data).show("fast");
        });
    });""" %{'reportsList':viewReportsList(script_s), 'script':script_s}

def viewReportElement(id, script_s):
    
    """ A function shows the important information for a Report as a row in a table """
    
    setup_all()
    report = reports.get_by(id = id)
    
    return """\
    <tr><td class="center-text"><span>%(id)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/reports?view=report&id=%(id)s"><span>%(title)s</span></a></td>\
    <td class="center-text"><span>%(customer)s</span></td>\
    <td class="center-text"><span>%(member)s</span></td>\
    <td class="center-text"><span>%(time)s</span></td>\
    <td class="center-text"><span>%(price)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/reports?view=edit&id=%(id)s" class="non-borders"><button>Edit</button></a></td>\
    <td class="center-text"><a href="%(script)s/page/reports?process=delete&id=%(id)s" class="non-borders"><button>Delete</button></a></td></tr> """ %{'id':report.id, 'title':report.title, 'customer':report.customer.name, 'member':report.member.username, 'time':report.time.strftime("%F %T"), 'price':report.price, 'script':script_s}
    
def viewReportsList(script_s):
    
    """ A function shows all Reports in the DB in a table """
    
    reportsList = """\
    <tr>\
    <th>ID</th>\
    <th>Title</th>\
    <th>Customer</th>\
    <th>Member</th>\
    <th>Time</th>\
    <th>Price</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr>\ """
    
    setup_all()
    
    for i in reports.query.all():
        reportsList += viewReportElement(id=i.id, script_s=script_s)
    return """\
    $("#reportsListTable").html('%s').show("fast");
    $("#reportsList").show("fast"); """ %reportsList 

def viewBillReportsList(bill, script_s):
    
    """ A function shows all Reports in the DB in a table """
    
    reportsList = """\
    <table border="1" cellspacing="0" cellpadding="0" class="bordered">\
    <tr>\
    <th>ID</th>\
    <th>Title</th>\
    <th>Customer</th>\
    <th>Member</th>\
    <th>Time</th>\
    <th>Price</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr>\ """
    
    setup_all()
    
    for i in reports.query.all():
        if i.bill == bill:
            reportsList += viewReportElement(id=i.id, script_s=script_s)
    
    reportsList += "</table>"
    return """\
    $("#billReports").html('%s').show("fast");""" %reportsList 

def processReportsResults(term, script_s):
    
    """ A function shows the Search Results in Reports Page """
    
    reportsList = """\
    <tr>\
    <th>ID</th>\
    <th>Title</th>\
    <th>Customer</th>\
    <th>Member</th>\
    <th>Time</th>\
    <th>Price</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr>\ """
    
    for i in reports.query.all():
        try:
            if term.startswith("customer: "):
                if i.customer.name == term[10:]:
                    reportsList += viewReportElement(id=i.id, script_s=script_s)
            elif term.startswith("member: "):
                if i.member.username == term[8:]:
                    reportsList += viewReportElement(id=i.id, script_s=script_s)
            elif term.startswith("price: "):
                if i.price == float(term[7:]):
                    reportsList += viewReportElement(id=i.id, script_s=script_s)
            elif term.startswith("date: "):
                if i.time.strftime("%F") == term[6:]:
                    reportsList += viewReportElement(i.id, script_s)
            elif term.startswith("datetime: "):
                if i.time.strftime("%F %H:%M") == term[10:]:
                    reportsList += viewReportElement(i.id, script_s)
            elif i.title.startswith(term):
                reportsList += viewReportElement(id=i.id, script_s=script_s)
            elif i.title.endswith(term):
                reportsList += viewReportElement(id=i.id, script_s=script_s)
            elif i.title.find(term) != -1:
                reportsList += viewReportElement(id=i.id, script_s=script_s)
            elif i.id == int(term):
                reportsList += viewReportElement(id=i.id, script_s=script_s)
        except ValueError: pass
    return """\
    $("#reportsResultsAjaxTable").html('%s').show("fast");
    $("#reportsResultsAjax").show("fast"); """ %reportsList 

def viewAddReport(bill_id, template_id, script_s):
    
    """ A function shows the Add Report Form and sends data to Reports Page """
    
    setup_all()
    bill = bills.get_by(id = bill_id)
    template = templates.get_by(id = template_id)
    
    content = filter_js_lines(filter_single_quotes(template.content))
    
    return """\
    document.addReport.process.value = "add";
    document.addReport.id.value = "";
    $("#customer_name").html('%(customer_name)s');
    $("#bill_id").html('%(bill_id)s');
    document.addReport.title.value = "%(template_title)s";
    document.addReport.price.value = "%(template_price)s";
    document.addReport.content_input.value = '%(template_content)s';
    $("div#addReport").show("fast");
    $("#backToReport").hide("fast");
    $("input[type=button]#submit").click(function() {
        var title = document.addReport.title.value;
        var is_inner = document.addReport.is_inner.value;
        var referred_by = document.addReport.referred_by.value;
        var price = document.addReport.price.value;
        contentInput.removeInstance('content_input');
        var content = document.addReport.content_input.value;
        var notes = document.addReport.notes.value;
        $.post("%(script)s/reports/", {
        process: "add",
        id: "",
        bill_id: "%(bill_id)s",
        title: title,
        is_inner: is_inner,
        referred_by: referred_by,
        price: price,
        content: content,
        notes: notes
        }, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'customer_name':bill.customer.name, 'bill_id':bill.id, 'template_title':template.title, 'template_price':template.price, 'template_content':content, 'script':script_s}

def viewEditReport(id, script_s):
    
    """ A function shows the Edit Report form and sends data to Report Page """
    
    setup_all()
    report = reports.get_by(id = id)
    title = report.title
    is_inner = report.is_inner
    referred_by = report.referred_by
    price = report.price
    content = report.content
    notes = report.notes
    
    content = filter_js_lines(filter_single_quotes(content))
    notes = filter_js_lines(filter_single_quotes(notes))
    
    return """\
    $("div#addReport h1").html("Edit Report");
    document.addReport.submit.value = "Edit Report";
    $("#customer_name").html('%(customer_name)s');
    $("#bill_id").html('%(bill_id)s');
    document.addReport.title.value = "%(title)s";
    document.addReport.is_inner.value = "%(is_inner)s";
    document.addReport.referred_by.value = "%(referred_by)s";
    document.addReport.price.value = %(price)s;
    $("#content_input").text('%(content)s');
    $("#notes").text('%(notes)s');
    document.getElementById("backToReport").href += "%(id)s";
    $("div#addReport").show("fast");
    $("input[type=button]#submit").click(function() {
        var title = document.addReport.title.value;
        var is_inner = document.addReport.is_inner.value;
        var referred_by = document.addReport.referred_by.value;
        var price = document.addReport.price.value;
        contentInput.removeInstance('content_input');
        var content = document.addReport.content_input.value;
        var notes = document.addReport.notes.value;
        $.post("%(script)s/reports/", {
        process: "edit",
        id: %(id)s,
        title: title,
        is_inner: is_inner,
        referred_by: referred_by,
        price: price,
        content: content,
        notes: notes
        }, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'customer_name':report.customer.name, 'bill_id':report.bill.id, 'id':id, 'title':title, 'is_inner':is_inner, 'referred_by':referred_by, 'price':price, 'content':content, 'notes':notes, 'script':script_s}

def viewReport(id, script_s):
    
    """ A function show the Report Information in a Table """
    
    setup_all()
    report = reports.get_by(id = id)
    is_inner = "Outer"
    if report.is_inner: is_inner = "Inner"
    
    content_nolines = report.content.splitlines()
    content = filter_single_quotes("".join(content_nolines))
    
    notes = filter_html_lines(filter_single_quotes(report.notes))
    
    return """\
    $("#view_id").html("%(id)s");
    $("#view_title").html("%(title)s");
    $("#view_customer_name").html("%(customer_name)s");
    $("#view_bill_id").html("%(bill_id)s");
    $("#view_member_name").html("%(member_name)s");
    $("#view_time").html("%(time)s");
    $("#view_is_inner").html("%(is_inner)s");
    $("#view_referred_by").html("%(referred_by)s");
    $("#view_price").html("%(price)s");
    $("#view_content").html('%(content)s');
    $("#view_notes").html('%(notes)s');
    document.getElementById("editBtn").href += "%(id)s";
    document.getElementById("backToBill").href += "%(bill_id)s";
    $("#viewReport").show("fast"); 
    $("#deleteBtn").click(function() {
        s = confirm("Are You Sure You Want to Delete this Report? ")
        if (s) {
            $.post("%(script)s/reports/", {process: "delete", id: "%(id)s"}, function(data) {
                $("#content").html(data).show("fast");
            });
        };
    });""" %{'id':report.id, 'title':report.title, 'customer_name':report.customer.name, 'bill_id':report.bill.id, 'member_name':report.member.username, 'time':report.time.strftime("%F %T"), 'is_inner':is_inner, 'referred_by':report.referred_by, 'price':report.price, 'content':content, 'notes':notes, 'script':script_s}

def viewDeletedReport(id):
    
    """ Small function that shows small message tells you that the Report was deleted Successfully """
    
    setup_all()
    report = reports.get_by(id = id)
    report.bill.total -= report.price
    total_after = report.bill.total - (report.bill.total * report.bill.discount)
    report.bill.rest = total_after - report.bill.paid
    report.delete()
    session.commit()
    
    return """\
    $("#deleted").show("fast"); """

def viewTemplatesList(bill_id, script_s):
    
    """ A function show a table contain all templates that will choose from """
    
    templatesList = """\
    <table border="1" cellspacing="0" cellpadding="0" class="bordered">\
    <tr>\
    <th>ID</th>\
    <th>Title</th>\
    <th>From Age</th>\
    <th>To Age</th>\
    <th>Price</th>\
    <th>Choose</th>\
    <tr>\ """
    
    setup_all()
    
    for i in templates.query.all():
        templatesList += viewTemplateElement(id=i.id, bill_id=bill_id, title=i.title, fromAge=i.from_age, toAge=i.to_age, price=i.price, script_s=script_s)
    
    templatesList += "</table>"
    
    return """\
    $("#templatesList").html('%s').show("fast");
    $("#chooseTemplate").show("fast"); """ %templatesList 

def viewTemplateElement(id, bill_id, title, fromAge, toAge, price, script_s):
    
    """ A function shows the important information for a Template as a row in a table """
    
    return """\
    <tr><td><span>%(id)s</span></td>\
    <td><a href="%(script)s/page/templates?view=template&id=%(id)s"><span>%(title)s</span></a></td>\
    <td class="center-text"><span>%(fromAge)s</span></td>\
    <td class="center-text"><span>%(toAge)s</span></td>\
    <td class="center-text"><span>%(price)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/reports?view=add&bill_id=%(bill_id)s&template_id=%(id)s" class="non-borders"><button>Choose</button></a></td></tr> """ %{'id':id, 'title':title, 'fromAge':fromAge, 'toAge':toAge, 'price':price, 'script':script_s, 'bill_id':bill_id}
