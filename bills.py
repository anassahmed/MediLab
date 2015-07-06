#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: bills.py: javascript functions for Medilab Web App
# By: Anass Ahmed

"""
a lot of javascript functions that control the Bills Pages Appearance.
"""

import datetime
from db import *
from okasha.baseWebApp import *
from functions import *
from reports import *

def viewBillsPage(script_s, query):
    
    """ A small function shows the main Bills page """
    
    return """\
    $.get("%(script)s/bills/?%(query)s", function(data) {
        $("#content").html(data).show("fast");
	}); """ %{'script':script_s, 'query':query}
    

def viewMainBillsPage(script_s):
    
    """ A function shows the Main Bills Page """
    
    return """\
    %(billsList)s
    $("#billsPage").show("fast"); 
    $("#searchBtn").click(function() {
        $("#billsList").hide("fast");
        $("#viewBillsResults").hide("fast").html("");
        var term = document.searchForm.term.value;
        $.get("%(script)s/bills/", {view: "search", term: term}, function(data) {
            $("#viewBillsResults").html(data).show("fast");
        });
    });
    $("#resetBtn").click(function() {
        $("#viewBillsResults").hide("fast");
        $("#billsList").show("fast"); 
    });""" %{'billsList':viewBillsList(script_s), 'script':script_s}

def viewBillElement(id, script_s):
    
    """ A function shows a bill as a row or record in a table. """
    
    setup_all()
    bill = bills.get_by(id = id)
    
    return """\
    <tr>\
    <td class="center-text"><a href="%(script)s/page/bills?view=bill&id=%(id)s"><span>%(id)s</span></a></td>\
    <td class="center-text"><a href="%(script)s/page/bills?view=bill&id=%(id)s"><span>%(customer)s</span></a></td>\
    <td class="center-text"><span>%(member)s</span></td>\
    <td class="center-text"><span>%(time)s</span></td>\
    <td class="center-text"><span>%(paid)s</span></td>\
    <td class="center-text"><span>%(rest)s</span></td>\
    <td class="center-text"><span>%(discount)s</span></td>\
    <td class="center-text"><span>%(total)s</span></td>\
    <td class="center-text"><a href="%(script)s/page/reports?view=choose&bill_id=%(id)s" class="non-borders"><button>Add</button></a></td>\
    <td class="center-text"><a href="%(script)s/page/bills?view=edit&id=%(id)s" class="non-borders"><button>Edit</button></a></td>\
    <td class="center-text"><a href="%(script)s/page/bills?process=delete&id=%(id)s" class="non-borders"><button>Delete</button></a></td>\
    <tr>""" %{'id':bill.id, 'customer':bill.customer.name, 'member':bill.member.username, 'time':bill.time.strftime("%F %T"), 'paid':bill.paid, 'rest':bill.rest, 'discount':bill.discount, 'total':bill.total, 'script':script_s}

def viewBillsList(script_s):
    
    """ A function shows all bills in a table. """
    
    billsList = """\
    <tr>\
    <th>ID</th>\
    <th>Customer</th>\
    <th>Member</th>\
    <th>Time</th>\
    <th>Paid</th>\
    <th>Rest</th>\
    <th>Discount</th>\
    <th>Total</th>\
    <th>Report</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr> """
    
    setup_all()
    for i in bills.query.all():
        billsList += viewBillElement(i.id, script_s)
    return """\
    $("#billsListTable").html('%s');
    $("#billsList").show("fast"); """ %billsList

def viewCustomerBillsList(customer_id, script_s):
    
    """ A function shows all bills for a selected customers """
    
    billsList = """\
    <tr>\
    <th>ID</th>\
    <th>Customer</th>\
    <th>Member</th>\
    <th>Time</th>\
    <th>Paid</th>\
    <th>Rest</th>\
    <th>Discount</th>\
    <th>Total</th>\
    <th>Report</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr> """
    
    setup_all()
    for i in bills.query.all():
        if i.customer.id == customer_id:
            billsList += viewBillElement(i.id, script_s)
    return """\
    $("#customerBillsTable").html('%s');
    $("#customerBills").show("fast"); """ %billsList

def processBillsResults(term, script_s):
    
    """ A function shows the Resutls table """
    
    billsList = """\
    <tr>\
    <th>ID</th>\
    <th>Customer</th>\
    <th>Member</th>\
    <th>Time</th>\
    <th>Paid</th>\
    <th>Rest</th>\
    <th>Discount</th>\
    <th>Total</th>\
    <th>Report</th>\
    <th>Edit</th>\
    <th>Delete</th>\
    <tr> """
    firstResults = ""
    secondResults = ""
    
    setup_all()
    for i in bills.query.all():
        try: 
            if term.startswith("[Rest]"):
                if i.rest > 0:
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("paid: "):
                if i.paid == float(term[6:]):
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("discount: "):
                if i.discount == float(term[10:]):
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("total: "):
                if i.total == float(term[7:]):
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("customer: "):
                if i.customer.name == term[10:]:
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("member: "):
                if i.member.username == term[8:]:
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("date: "):
                if i.time.strftime("%F") == term[6:]:
                    firstResults += viewBillElement(i.id, script_s)
            elif term.startswith("datetime: "):
                if i.time.strftime("%F %H:%M") == term[10:]:
                    firstResults += viewBillElement(i.id, script_s)
            elif i.customer.name.startswith(term):
                firstResults += viewBillElement(i.id, script_s)
            elif i.customer.name.endswith(term):
                secondResults += viewBillElement(i.id, script_s)
            elif i.customer.name.find(term) != -1:
                secondResults += viewBillElement(i.id, script_s)
            elif i.id == int(term):
                firstResults += viewBillElement(i.id, script_s)
        except ValueError: pass
    billsList += firstResults + secondResults
    return """\
    $("#billsResultsAjaxTable").html('%s');
    $("#billsResultsAjax").show("fast"); """ %billsList

def viewBill(id, script_s):
    
    """ A function shows the Information of a bill """
    
    setup_all()
    bill = bills.get_by(id = id)
    customer = bill.customer.name
    customer_id = bill.customer.id
    member = bill.member.username
    time = bill.time.strftime("%F %T")
    paid = bill.paid
    rest = bill.rest
    discount = bill.discount
    total = bill.total
    notes = bill.notes
    
    total_after = total - (total * discount)
    if notes == None: notes = ""
    notes = filter_html_lines(filter_single_quotes(notes))
    
    return """\
    $("#view_id").html("%(id)s");
    $("#view_customer_name").html("%(customer)s");
    $("#view_member_name").html("%(member)s");
    $("#view_time").html("%(time)s");
    $("#view_discount").html("%(discount)s");
    $("#view_paid").html("%(paid)s");
    $("#view_rest").html("%(rest)s");
    $("#view_total").html("%(total)s");
    $("#view_total_after_discount").html("%(total_after)s");
    $("#view_notes").html('%(notes)s');
    document.getElementById("editBtn").href += "%(id)s";
    document.getElementById("deleteBtn").href += "%(id)s";
    document.getElementById("addReportBtn").href += "%(id)s";
    document.getElementById("backToCustomer").href += "%(customer_id)s";
    %(reportsList)s
    $("#viewBill").show("fast"); """ %{'id':id, 'customer':customer, 'customer_id':customer_id, 'member':member, 'time':time, 'discount':discount, 'paid':paid, 'rest':rest, 'total':total, 'total_after':total_after, 'notes':notes, 'reportsList':viewBillReportsList(bill, script_s)}

def viewEditBill(id, script_s):
    
    """ A function that shows the Edit form and fill it with the information """
    setup_all()
    bill = bills.get_by(id = id)
    customer = bill.customer.name
    paid = bill.paid
    discount = bill.discount
    notes = bill.notes
    
    if notes == None: notes = " "
    notes = filter_js_lines(filter_single_quotes(notes))
    
    return """\
    $("#customer_name").html("%(customer)s");
    document.editBill.discount.value = "%(discount)s";
    document.editBill.paid.value = "%(paid)s";
    document.editBill.notes.value = '%(notes)s';
    document.getElementById('backToBill').href += "%(id)s";
    $("#editBill").show("fast"); 
    $("#submit").click(function() {
        var discount = document.editBill.discount.value;
        var paid = document.editBill.paid.value;
        var notes = document.editBill.notes.value;
        $.get("%(script)s/bills/", {
        process: "edit",
        id: %(id)s,
        discount: discount,
        paid: paid,
        notes: notes}, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'id':id, 'customer':customer, 'discount':discount, 'paid':paid, 'notes':notes, 'script':script_s}

def viewDeletedBill(id):
    
    """ A small function shows a small message tells user that the requested bill was deleted successfully. """
    
    setup_all()
    bill = bills.get_by(id = id)
    for i in bill.reports:
        if i != None:
            i.delete()
    bill.delete()
    session.commit()
    
    return """\
    $("#deleted").show("fast"); """
