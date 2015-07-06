#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: settings.py: JS functions control Appearance of Settings Pages

from db import *
from functions import *

def checkNone(obj):
    if obj == None: obj = "None"
    else: obj = obj.value
    return obj

def viewSettingsPage(script_s, query):
    
    """ A small function shows the main Settings Page """
    
    return """\
    $.get("%(script)s/settings/?%(query)s", function(data) {
        $("#content").html(data).show("fast");
    }); """ %{'script': script_s, 'query': query}

def viewMainSettingsPage():
    
    """ A function shows the main Settings Page """
    
    setup_all()
    
    lab_name = LabInfo.get_by(name = u"lab_name")
    lab_name = checkNone(lab_name)
    lab_address = LabInfo.get_by(name = u"lab_address")
    lab_address = filter_html_lines(checkNone(lab_address))
    lab_phone = LabInfo.get_by(name = u"lab_phone")
    lab_phone = checkNone(lab_phone)
    lab_email = LabInfo.get_by(name = u"lab_email")
    lab_email = checkNone(lab_email)
    lab_website = LabInfo.get_by(name = u"lab_website")
    lab_website = checkNone(lab_website)
    top_margin = LabInfo.get_by(name = u"print_top_margin")
    top_margin = checkNone(top_margin)
    bottom_margin = LabInfo.get_by(name = u"print_bottom_margin")
    bottom_margin = checkNone(bottom_margin)
    right_margin = LabInfo.get_by(name = u"print_right_margin")
    right_margin = checkNone(right_margin)
    left_margin = LabInfo.get_by(name = u"print_left_margin")
    left_margin = checkNone(left_margin)
    print_report_details = LabInfo.get_by(name = u"print_report_details")
    print_report_details = checkNone(print_report_details)
    
    if int(print_report_details): print_report_details = "Yes"
    else: print_report_details = "No"
    
    return """\
    $("#view_lab_name").html("%(lab_name)s");
    $("#view_lab_address").html('%(lab_address)s');
    $("#view_lab_phone").html("%(lab_phone)s");
    $("#view_lab_email").html("%(lab_email)s");
    $("#view_lab_website").html("%(lab_website)s");
    $("#view_print_top_margin").html("%(top_margin)s");
    $("#view_print_bottom_margin").html("%(bottom_margin)s");
    $("#view_print_right_margin").html("%(right_margin)s");
    $("#view_print_left_margin").html("%(left_margin)s");
    $("#view_print_report_details").html("%(print_report_details)s"); 
    $("#mainPage").show("fast");""" %{'lab_name':lab_name, 'lab_address':lab_address, 'lab_phone':lab_phone, 'lab_email':lab_email, 'lab_website':lab_website, 'top_margin': top_margin, 'bottom_margin': bottom_margin, 'right_margin': right_margin, 'left_margin':left_margin, 'print_report_details': print_report_details}
    
def viewEditLabInfo(script_s):
    
    setup_all()
    
    lab_name = LabInfo.get_by(name = u"lab_name")
    lab_name = checkNone(lab_name)
    lab_address = LabInfo.get_by(name = u"lab_address")
    lab_address = filter_js_lines(checkNone(lab_address))
    lab_phone = LabInfo.get_by(name = u"lab_phone")
    lab_phone = checkNone(lab_phone)
    lab_email = LabInfo.get_by(name = u"lab_email")
    lab_email = checkNone(lab_email)
    lab_website = LabInfo.get_by(name = u"lab_website")
    lab_website = checkNone(lab_website)
    
    return """\
    document.getElementById("lab_name").value = "%(lab_name)s";
    $("#lab_address").text('%(lab_address)s');
    document.getElementById("lab_phone").value = "%(lab_phone)s";
    document.getElementById("lab_email").value = "%(lab_email)s";
    document.getElementById("lab_website").value = "%(lab_website)s";
    $("#editLabInfo").show("fast"); 
    $("#editLabInfo #submit").click(function() {
        var lab_name = document.getElementById("lab_name").value;
        var lab_address = document.getElementById("lab_address").value;
        var lab_phone = document.getElementById("lab_phone").value;
        var lab_email = document.getElementById("lab_email").value;
        var lab_website = document.getElementById("lab_website").value;
        $.post("%(script)s/settings/", {
        process: "edit",
        name: "labinfo",
        lab_name: lab_name,
        lab_address: lab_address,
        lab_phone: lab_phone,
        lab_email: lab_email,
        lab_website: lab_website}, function(data) {
            $("#content").html(data).show("fast");
        });
    }); """ %{'lab_name':lab_name, 'lab_address':lab_address, 'lab_phone':lab_phone, 'lab_email':lab_email, 'lab_website':lab_website, 'script':script_s}
    
def viewEditPrinting(script_s):
    
    """ A function shows the Edit form for Printing Settings """
    
    setup_all()
    
    top_margin = LabInfo.get_by(name = u"print_top_margin")
    top_margin = checkNone(top_margin)
    bottom_margin = LabInfo.get_by(name = u"print_bottom_margin")
    bottom_margin = checkNone(bottom_margin)
    right_margin = LabInfo.get_by(name = u"print_right_margin")
    right_margin = checkNone(right_margin)
    left_margin = LabInfo.get_by(name = u"print_left_margin")
    left_margin = checkNone(left_margin)
    print_report_details = LabInfo.get_by(name = u"print_report_details")
    print_report_details = checkNone(print_report_details)
    if print_report_details == "None": print_report_details = 0
    
    return """\
    document.getElementById("print_top_margin").value = "%(top_margin)s";
    document.getElementById("print_bottom_margin").value = "%(bottom_margin)s";
    document.getElementById("print_right_margin").value = "%(right_margin)s";
    document.getElementById("print_left_margin").value = "%(left_margin)s";
    var default_report_details = %(print_report_details)s;
    if (default_report_details == 1) {document.getElementById("print_report_details").checked = true;}
    $("#editPrintSettings").show("fast"); 
    $("#editPrintSettings #submit").click(function() {
        var top_margin = document.getElementById("print_top_margin").value;
        var bottom_margin = document.getElementById("print_bottom_margin").value;
        var right_margin = document.getElementById("print_right_margin").value;
        var left_margin = document.getElementById("print_left_margin").value;
        var print_report_details = 0;
        if (document.getElementById("print_report_details").checked) {
            var print_report_details = 1;
        };
        $.post("%(script)s/settings/", {
        process: "edit",
        name: "printing",
        print_top_margin: top_margin,
        print_bottom_margin: bottom_margin,
        print_right_margin: right_margin,
        print_left_margin: left_margin,
        print_report_details: print_report_details}, function(data) {
            $("#content").html(data).show("fast");
        });
    });""" %{'top_margin':top_margin, 'bottom_margin':bottom_margin, 'right_margin':right_margin, 'left_margin':left_margin, 'print_report_details':print_report_details, 'script':script_s}
