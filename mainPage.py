#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: reports.py: javascript functions for Medilab Web App
# By: Anass Ahmed

""" A lot of JS Appearance and Effects for main Page """

from customers import *
from bills import *

def viewMainMainPage(rq):
    
    """ view Main Page """
    
    setup_all()
    
    customers_count = len(customers.query.all())
    bills_count = len(bills.query.all())
    reports_count = len(reports.query.all())
    customersList = customers.query.all()
    customersList.reverse()
    if len(customersList) < 10: customersListFinal = customersList
    else: customersListFinal = customersList[0:10]
    latestCustomers = """\
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
    
    for i in customersListFinal:
        latestCustomers += viewCustomerElement(i.id, i.name, i.birth, i.gender, len(i.bills), len(i.reports), rq.script)
    billsList = bills.query.all()
    billsList.reverse()
    if len(billsList) < 10: billsListFinal = billsList
    else: billsListFinal = billsList[0:10]
    latestBills = """\
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
    
    for i in billsListFinal:
        latestBills += viewBillElement(i.id, rq.script)
    
    return """\
    $("#customers").html("%(customers)s");
    $("#bills").html("%(bills)s");
    $("#reports").html("%(reports)s");
    $("#latestCustomers").html('%(latestCustomers)s');
    $("#latestBills").html('%(latestBills)s'); """ %{'customers':customers_count, 'bills':bills_count, 'reports':reports_count, 'latestCustomers':latestCustomers, 'latestBills':latestBills}
