#_*_ coding: UTF-8 _*_
#!/usr/bin/python
"""
Main file of MediLab Orginaizer Program.
"""

from okasha.baseWebApp import *
from db import *
from functions import *
from customers import *
from templates import *
from bills import *
from reports import *
from settings import *
from session import *
from members import *
from mainPage import *
from sqlalchemy import exceptions
import sys, os, os.path, datetime, hashlib, time, random, urllib

class MediLab(baseWebApp):
    def __init__(self, *args, **kw):
        baseWebApp.__init__(self, *args, **kw)
    @expose(percentTemplate, ['index.html'])
    def _root(self, rq, *args):
        setup_all()
        contentScript = viewMainPage(rq.script)
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        if args:
            if args[0] == 'page':
                if args[1] == "about":
                    contentScript = viewAboutPage(rq.script)
                if args[1] == "customers":
                    if rq.q.has_key("view"):
                        query = "view="+rq.q.getfirst("view","")+"&id="+rq.q.getfirst("id","")
                    elif rq.q.has_key("process"):
                        query = "process="+rq.q.getfirst("process","")+"&id="+rq.q.getfirst("id","")
                    else: query = ""
                    contentScript = viewCustomersPage(rq.script, query)
                elif args[1] == "templates":
                    if rq.q.has_key("view"):
                        query = "view="+rq.q.getfirst("view","")+"&id="+rq.q.getfirst("id","")
                    elif rq.q.has_key("process"):
                        query = "process="+rq.q.getfirst("process","")+"&id="+rq.q.getfirst("id","")
                    else: query = ""
                    contentScript = viewTemplatesPage(rq.script, query)
                elif args[1] == "bills":
                    if rq.q.has_key("view"):
                        query = "view="+rq.q.getfirst("view","")+"&id="+rq.q.getfirst("id","")
                    elif rq.q.has_key("process"):
                        query = "process="+rq.q.getfirst("process","")+"&id="+rq.q.getfirst("id","")
                    else: query = ""
                    contentScript = viewBillsPage(rq.script, query)
                elif args[1] == "reports":
                    try:
                        if rq.q.has_key("view"):
                            bill_id = ""; template_id = ""
                            if rq.q.getfirst("bill_id","") != None: bill_id = rq.q.getfirst("bill_id","")
                            if rq.q.getfirst("template_id","") != None: template_id = rq.q.getfirst("template_id","")
                            query = "view="+rq.q.getfirst("view","")+"&id="+rq.q.getfirst("id","")+"&bill_id="+bill_id+"&template_id="+template_id
                        elif rq.q.has_key("process"):
                            query = "process="+rq.q.getfirst("process","")+"&id="+rq.q.getfirst("id","")+"&bill_id="+rq.q.getfirst("bill_id","")
                        else: query = ""
                        contentScript = viewReportsPage(rq.script, query)
                    except TypeError: pass
                elif args[1] == "settings":
                    if rq.q.has_key("view"):
                        query = "view="+rq.q.getfirst("view","")+"&name="+rq.q.getfirst("name","")
                    elif rq.q.has_key("process"):
                        query = "process"+rq.q.getfirst("process","")+"&name="+rq.q.getfirst("name","")
                    else: query = ""
                    contentScript = viewSettingsPage(rq.script, query)
                elif args[1] == "members":
                    if rq.q.has_key("view"):
                        query = "view="+rq.q.getfirst("view","")+"&id="+rq.q.getfirst("id","")
                    elif rq.q.has_key("process"):
                        query = "process="+rq.q.getfirst("process","")+"&id="+rq.q.getfirst("id","")
                    else: query = ""
                    contentScript = viewMembersPage(rq.script, query)
        else:
            contentScript = viewMainPage(rq.script)
        return {'contentScript':contentScript, 'script':rq.script}
    @expose(percentTemplate, ['main.html'])
    def main(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/'+u'main'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        mainScript = viewMainMainPage(rq)
        return {'mainScript':mainScript, 'script':rq.script}
    @expose(percentTemplate, ['install.html'])
    def install(self, rq, *args):
        setup_all()
        registerForm = "display:none;";
        registerSuccess = "display:none;";
        try:
            admin = members.get_by(is_admin=1)
            if admin != None: raise forbiddenException()
        except exceptions.OperationalError as e:
            if rq.q.has_key('username'):
                if rq.q.getfirst('email') == None:
                    email = ""
                else: email = rq.q.getfirst('email').decode('utf8')
                if rq.q.getfirst('phone') == None:
                    phone = ""
                else: phone = rq.q.getfirst('phone').decode('utf8')
                create_all()
                members(username = rq.q.getfirst('username').decode('utf8'),
                password = hashlib.sha256(rq.q.getfirst('password').decode('utf8')).hexdigest().decode('utf8'),
                email = rq.q.getfirst('email').decode('utf8'),
                phone = rq.q.getfirst('phone').decode('utf8'),
                is_admin = 1,
                is_banned = 0
                )
                session.commit()
                registerSuccess = "";
            else:
                registerForm = "";
        return {
        'script':rq.script,
        'registerForm':registerForm,
        'registerSuccess':registerSuccess
        }
    @expose(percentTemplate, ['session.html'])
    def session(self, rq, *args):
        setup_all()
        sessionScript = "" + addReturnUrl(rq.q.getfirst("returnUrl",""))
        if rq.q.has_key('do'):
            if rq.q.getfirst('do') == 'logout':
                login_session = sessions.get_by(session_hash = rq.cookies['medilab_session'].value.decode('utf8'))
                if login_session != None: 
                    login_session.delete()
                    session.commit()
                    rq.response.setCookie('medilab_session', '', 0)
                    raise redirectException(rq.script+"/session/?logout=1")
        if rq.cookies.has_key("medilab_session"): raise redirectException(rq.script+"/")
        if rq.q.has_key('logout'): sessionScript = viewLoggedOut()
        if rq.q.has_key('username'):
            if rq.q.getfirst('password') == None: raise redirectException(rq.script+"/")
            member = members.get_by(username = rq.q.getfirst('username').decode('utf8'))
            if member == None: 
                sessionScript = viewUserError() + addReturnUrl(rq.q.getfirst("returnUrl",""))
            elif member.password != hashlib.sha256(rq.q.getfirst('password').decode('utf8')).hexdigest().decode('utf8'): sessionScript = viewPassError() + addReturnUrl(rq.q.getfirst("returnUrl",""))
            elif member.is_banned: sessionScript = viewBanError(member.id)
            else:
                is_cookie = 0
                if rq.q.has_key('cookie'): is_cookie = 1
                login_session = sessions(
                username = member.username,
                is_cookie = is_cookie,
                time = datetime.datetime.now(),
                session_hash = hashlib.sha256(str(random.randint(00000000000000000000, 99999999999999999999))).hexdigest().decode('utf8')
                )
                session.commit()
                session_hash = login_session.session_hash
                if not is_cookie: rq.response.setCookie('medilab_session', session_hash, 60*30)
                else: rq.response.setCookie('medilab_session', session_hash, 60*60*24*14)
                if rq.q.has_key('returnUrl'): raise redirectException(rq.script+rq.q.getfirst('returnUrl'))
                raise redirectException(rq.script+"/")
        return {
        'script': rq.script,
        'sessionScript': sessionScript
        }
    @expose(percentTemplate, ['customers.html'])
    def customers(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/customers/'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        setup_all()
        customerScript = viewMainCustomersPage(rq.script)
        if rq.q.has_key("view"):
            if escape(rq.q.getfirst("view","")) == "add":
                customerScript = viewAddCustomer(rq.script)
            elif escape(rq.q.getfirst("view","")) == "edit":
                customer = customers.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if customer == None: raise fileNotFoundException()
                customerScript = viewEditCustomer(id = customer.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view", "")) == "customer":
                customer = customers.get_by(id = int(escape(rq.q.getfirst("id",""))))
                if customer == None: raise fileNotFoundException()
                customerScript = viewCustomer(id = customer.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "search":
                customerScript = viewCustomersResults(escape(rq.q.getfirst("term","").decode("utf8")), rq.script)
        if rq.q.has_key("process"):
            if escape(rq.q.getfirst("process","")) == "add":
                birth_d = int(escape(rq.q.getfirst("birth_d","")))
                birth_m = int(escape(rq.q.getfirst("birth_m","")))
                birth_y = int(escape(rq.q.getfirst("birth_y","")))
                customer = customers(
                name = escape(rq.q.getfirst("name","").decode("utf8")),
                birth = datetime.date(birth_y, birth_m, birth_d),
                gender = escape(rq.q.getfirst("gender","").decode("utf8")),
                phone = escape(rq.q.getfirst("phone","").decode("utf8")),
                address = escape(rq.q.getfirst("address","").decode("utf8")),
                notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                )
                session.commit()
                customerScript = 'window.location.replace("%(script)s/page/customers?view=customer&id=%(id)s");' %{'script':rq.script, 'id':customer.id}
            elif escape(rq.q.getfirst("process","")) == "edit":
                customer = customers.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if customer == None: raise fileNotFoundException()
                birth_d = int(escape(rq.q.getfirst("birth_d","")))
                birth_m = int(escape(rq.q.getfirst("birth_m","")))
                birth_y = int(escape(rq.q.getfirst("birth_y","")))
                customer.name = escape(rq.q.getfirst("name","").decode("utf8"))
                customer.birth = datetime.date(birth_y, birth_m, birth_d)
                customer.gender = escape(rq.q.getfirst("gender","").decode("utf8"))
                customer.phone = escape(rq.q.getfirst("phone","").decode("utf8"))
                customer.address = escape(rq.q.getfirst("address","").decode("utf8"))
                customer.notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                session.commit()
                customerScript = 'window.location.replace("%(script)s/page/customers?view=customer&id=%(id)s");' %{'script':rq.script, 'id':customer.id}
            elif escape(rq.q.getfirst("process","")) == "delete":
                customer = customers.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if customer == None: raise fileNotFoundException()
                customerScript = viewDeletedCustomer(customer.id)
        return {'customerScript':customerScript, 'script':rq.script}
    @expose(percentTemplate, ['bills.html'])
    def bills(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/bills/'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        setup_all()
        member = whoIsLogged(rq)
        billsScript = viewMainBillsPage(rq.script)
        if rq.q.has_key("view"):
            if escape(rq.q.getfirst("view","")) == "edit":
                bill = bills.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if bill == None: raise fileNotFoundException()
                billsScript = viewEditBill(bill.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "bill":
                bill = bills.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if bill == None: raise fileNotFoundException()
                billsScript = viewBill(id = bill.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "search":
                billsScript = processBillsResults(term = escape(rq.q.getfirst("term","")), script_s = rq.script)
        if rq.q.has_key("process"):
            if escape(rq.q.getfirst("process","")) == "add":
                new_bill = bills(
                customer = customers.get_by(id=int(escape(rq.q.getfirst("id","")))),
                member = member,
                time = datetime.datetime.now(),
                paid = 0,
                rest = 0,
                discount = 0,
                total = 0
                )
                session.commit()
                billsScript = 'window.location.replace("%(script)s/page/bills?view=bill&id=%(id)s");' %{'script':rq.script, 'id':new_bill.id}
            elif escape(rq.q.getfirst("process","")) == "edit":
                bill = bills.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if bill == None: raise fileNotFoundException()
                bill.member = member
                bill.time = datetime.datetime.now()
                bill.paid = float(escape(rq.q.getfirst("paid","")))
                bill.discount = float(escape(rq.q.getfirst("discount","")))
                bill.notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                total_after = bill.total - (bill.total * bill.discount)
                bill.rest = total_after - bill.paid
                session.commit()
                billsScript = 'window.location.replace("%(script)s/page/bills?view=bill&id=%(id)s");' %{'script':rq.script, 'id':bill.id}
            elif escape(rq.q.getfirst("process","")) == "delete":
                bill = bills.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if bill == None: raise fileNotFoundException()
                billsScript = viewDeletedBill(bill.id)
        return {'billsScript':billsScript, 'script':rq.script}
    @expose(percentTemplate, ['reports.html'])
    def reports(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/reports/'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        setup_all()
        member = whoIsLogged(rq)
        reportsScript = viewMainReportsPage(rq.script)
        if rq.q.has_key("view"):
            if escape(rq.q.getfirst("view","")) == "add":
                reportsScript = viewAddReport(int(escape(rq.q.getfirst("bill_id",""))), int(escape(rq.q.getfirst("template_id",""))), rq.script)
            elif escape(rq.q.getfirst("view","")) == "edit":
                report = reports.get_by(id = int(escape(rq.q.getfirst("id",""))))
                reportsScript = viewEditReport(id = report.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "report":
                reportsScript = viewReport(int(escape(rq.q.getfirst("id",""))), rq.script)
            elif escape(rq.q.getfirst("view","")) == "search":
                reportsScript = processReportsResults(escape(rq.q.getfirst("term","").decode("utf8")), rq.script)
            elif escape(rq.q.getfirst("view","")) == "choose":
                reportsScript = viewTemplatesList(bill_id = int(escape(rq.q.getfirst("bill_id",""))), script_s = rq.script)
        elif rq.q.has_key("process"):
            if escape(rq.q.getfirst("process","")) == "add":
                bill = bills.get_by(id = int(escape(rq.q.getfirst("bill_id",""))))
                new_report = reports(
                title = escape(rq.q.getfirst("title","").decode("utf8")),
                customer = bill.customer,
                bill = bill,
                member = member,
                content = rq.q.getfirst("content","").decode("utf8"),
                time = datetime.datetime.now(),
                is_inner = int(escape(rq.q.getfirst("is_inner",""))),
                referred_by = escape(rq.q.getfirst("referred_by","").decode("utf8")),
                price = float(escape(rq.q.getfirst("price",""))),
                notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                )
                bill.total += new_report.price
                total_after = bill.total - (bill.total * bill.discount)
                bill.rest = total_after - bill.paid
                session.commit()
                reportsScript = 'window.location.replace("%(script)s/page/reports?view=report&id=%(id)s");' %{'script':rq.script, 'id':new_report.id}
            elif escape(rq.q.getfirst("process","")) == "edit":
                report = reports.get_by(id = int(escape(rq.q.getfirst("id",""))))
                report.title = escape(rq.q.getfirst("title","").decode("utf8"))
                report.member = member
                report.content = rq.q.getfirst("content","").decode("utf8")
                report.time = datetime.datetime.now()
                report.is_inner = int(escape(rq.q.getfirst("is_inner","")))
                report.referred_by = escape(rq.q.getfirst("referred_by","").decode("utf8"))
                report.bill.total -= report.price
                report.price = float(escape(rq.q.getfirst("price","")))
                report.bill.total += report.price
                report.notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                total_after = report.bill.total - (report.bill.total * report.bill.discount)
                report.bill.rest = total_after - report.bill.paid
                session.commit()
                reportsScript = 'window.location.replace("%(script)s/page/reports?view=report&id=%(id)s");' %{'script':rq.script, 'id':report.id}
            elif escape(rq.q.getfirst("process","")) == "delete":
                report = reports.get_by(id = int(escape(rq.q.getfirst("id",""))))
                reportsScript = viewDeletedReport(report.id)
        return {'reportsScript':reportsScript, 'script':rq.script}
    @expose(percentTemplate, ['templates.html'])
    def templates(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/'+u'/templates/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        setup_all()
        templatesScript = viewMainTemplatesPage(rq.script)
        if rq.q.has_key("view"):
            if rq.q.getfirst("view","") == "add":
                templatesScript = viewAddTemplate(rq.script)
            elif escape(rq.q.getfirst("view","")) == "edit":
                template = templates.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if template == None: raise fileNotFoundException()
                templatesScript = viewEditTemplate(id = template.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "template":
                template = templates.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if template == None: raise fileNotFoundException()
                templatesScript = viewTemplate(id = template.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "search":
                templatesScript = processTemplatesResults(escape(rq.q.getfirst("term","").decode("utf8")), rq.script)
        if rq.q.has_key("process"):
            if escape(rq.q.getfirst("process","")) == "add":
                new_template = templates(
                title = escape(rq.q.getfirst("title","").decode("utf8")),
                from_age = int(escape(rq.q.getfirst("fromAge",""))),
                to_age = int(escape(rq.q.getfirst("toAge",""))),
                price = float(escape(rq.q.getfirst("price",""))),
                content = rq.q.getfirst("content","").decode("utf8"),
                notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                )
                session.commit()
                templatesScript = 'window.location.replace("%(script)s/page/templates?view=template&id=%(id)s");' %{'script':rq.script, 'id':new_template.id}
            elif escape(rq.q.getfirst("process","")) == "edit":
                template = templates.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if template == None: raise fileNotFoundException()
                template.title = escape(rq.q.getfirst("title","").decode("utf8"))
                template.from_age = int(escape(rq.q.getfirst("fromAge","")))
                template.to_age = int(escape(rq.q.getfirst("toAge","")))
                template.price = float(escape(rq.q.getfirst("price","")))
                template.content = rq.q.getfirst("content","").decode("utf8")
                template.notes = escape(rq.q.getfirst("notes","").decode("utf8"))
                session.commit()
                templatesScript = 'window.location.replace("%(script)s/page/templates?view=template&id=%(id)s");' %{'script':rq.script, 'id':template.id}
            elif escape(rq.q.getfirst("process","")) == "delete":
                template = templates.get_by(id=int(escape(rq.q.getfirst("id",""))))
                if template == None: raise fileNotFoundException()
                templatesScript = viewDeletedTemplate(template.id)
        return {'templatesScript':templatesScript, 'script':rq.script}
    @expose(percentTemplate, ['members.html'])
    def members(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/members/'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        if not userLoggedisAdmin(rq): raise forbiddenException()
        membersScript = viewMainMembersPage(rq.script)
        if rq.q.has_key("view"):
            if escape(rq.q.getfirst("view","")) == "add":
                membersScript = viewAddMember(rq.script)
            elif escape(rq.q.getfirst("view","")) == "edit":
                member = members.get_by(id = int(escape(rq.q.getfirst("id",""))))
                if member == None: raise fileNotFoundException()
                membersScript = viewEditMember(id = member.id, script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "member":
                member = members.get_by(id = int(rq.q.getfirst("id","")))
                if member == None: raise fileNotFoundException()
                membersScript = viewMember(member.id)
            elif escape(rq.q.getfirst("view","")) == "search":
                membersScript = processMemberResults(term = escape(rq.q.getfirst("term","").decode("utf8")), script_s = rq.script)
            elif escape(rq.q.getfirst("view","")) == "deleted":
                membersScript += "\n$('#deleted').show()"
        elif rq.q.has_key("process"):
            if escape(rq.q.getfirst("process")) == "add":
                new_member = members(
                username = escape(rq.q.getfirst("username","").decode("utf8")),
                password = hashlib.sha256(escape(rq.q.getfirst("password").decode('utf8'))).hexdigest(),
                email = escape(rq.q.getfirst("email","").decode("utf8")),
                phone = escape(rq.q.getfirst("phone","").decode("utf8")),
                is_admin = int(escape(rq.q.getfirst("is_admin","").decode("utf8")))
                )
                session.commit()
                membersScript = "window.location.replace('%(script)s/page/members/?view=member&id=%(id)s');" %{'script':rq.script, 'id':new_member.id}
            elif escape(rq.q.getfirst("process","")) == "edit":
                member = members.get_by(id = int(escape(rq.q.getfirst("id",""))))
                if member == None: raise fileNotFoundException()
                member.username = escape(rq.q.getfirst("username","").decode("utf8"))
                if rq.q.getfirst("password") == None or rq.q.getfirst("password") == "": pass
                else: member.password = hashlib.sha256(escape(rq.q.getfirst("password").decode('utf8'))).hexdigest()
                member.email = escape(rq.q.getfirst("email","").decode("utf8"))
                member.phone = escape(rq.q.getfirst("phone","").decode("utf8"))
                member.is_admin = int(escape(rq.q.getfirst("is_admin","")))
                member.is_banned = int(escape(rq.q.getfirst("is_banned","")))
                member.ban_reason = escape(rq.q.getfirst("ban_reason","").decode("utf8"))
                session.commit()
                membersScript = "window.location.replace('%(script)s/page/members/?view=member&id=%(id)s');" %{'script':rq.script, 'id':member.id}
            elif escape(rq.q.getfirst("process","")) == "delete":
                member = members.get_by(id = int(escape(rq.q.getfirst("id",""))))
                if member == None: raise fileNotFoundException()
                membersScript = viewDeletedMember(id = member.id, script_s = rq.script)
        return {'membersScript':membersScript, 'script':rq.script}
    @expose(percentTemplate, ['settings.html'])
    def settings(self, rq, *args):
        returnUrl = urllib.quote(rq.script.decode("utf8")+u'/settings/'+u'/'.join(args).decode("utf8")+u'?'+rq.qs.decode("utf8"))
        if not userLoggedin(rq) and returnUrl != u"/?": raise redirectException(rq.script+"/session/?returnUrl=%s" %returnUrl)
        elif not userLoggedin(rq): raise redirectException(rq.script+"/session/")
        setup_all()
        settingsScript = viewMainSettingsPage()
        if rq.q.has_key("view"):
            if escape(rq.q.getfirst("view","")) == "edit" and escape(rq.q.getfirst("name","")) == "labinfo":
                if not userLoggedisAdmin(rq): raise forbiddenException()
                settingsScript = viewEditLabInfo(rq.script)
            elif escape(rq.q.getfirst("view","")) == "edit" and escape(rq.q.getfirst("name","")) == "printing":
                settingsScript = viewEditPrinting(rq.script)
        elif rq.q.has_key("saved"): viewMainSettingsPage()
        elif rq.q.has_key("process"):
            if escape(rq.q.getfirst("process","")) == "edit" and escape(rq.q.getfirst("name","")) == "labinfo":
                if not userLoggedisAdmin(rq): raise forbiddenException()
                test = LabInfo.get_by(name = u"lab_name")
                if test == None:
                    LabInfo(name = u"lab_name", value = escape(rq.q.getfirst("lab_name","").decode("utf8")))
                    LabInfo(name = u"lab_address", value = escape(rq.q.getfirst("lab_address","").decode("utf8")))
                    LabInfo(name = u"lab_phone", value = escape(rq.q.getfirst("lab_phone","").decode("utf8")))
                    LabInfo(name = u"lab_email", value = escape(rq.q.getfirst("lab_email","").decode("utf8")))
                    LabInfo(name = u"lab_website", value = escape(rq.q.getfirst("lab_website","").decode("utf8")))
                    session.commit()
                else:
                    lab_name = LabInfo.get_by(name = u"lab_name")
                    lab_name.value = escape(rq.q.getfirst("lab_name","").decode("utf8"))
                    lab_address = LabInfo.get_by(name = u"lab_address")
                    lab_address.value = escape(rq.q.getfirst("lab_address","").decode("utf8"))
                    lab_phone = LabInfo.get_by(name = u"lab_phone")
                    lab_phone.value = escape(rq.q.getfirst("lab_phone","").decode("utf8"))
                    lab_email = LabInfo.get_by(name = u"lab_email")
                    lab_email.value = escape(rq.q.getfirst("lab_email","").decode("utf8"))
                    lab_website = LabInfo.get_by(name = u"lab_website")
                    lab_website.value = escape(rq.q.getfirst("lab_website","").decode("utf8"))
                    session.commit()
                settingsScript = "window.location.replace('%(script)s/page/settings/');" %{'script':rq.script}
            elif escape(rq.q.getfirst("process","")) == "edit" and escape(rq.q.getfirst("name","")) == "printing":
                test = LabInfo.get_by(name = u"print_top_margin")
                if test == None:
                    LabInfo(name = u"print_top_margin", value = escape(rq.q.getfirst("print_top_margin","").decode("utf8")))
                    LabInfo(name = u"print_bottom_margin", value = escape(rq.q.getfirst("print_bottom_margin","").decode("utf8")))
                    LabInfo(name = u"print_right_margin", value = escape(rq.q.getfirst("print_right_margin","").decode("utf8")))
                    LabInfo(name = u"print_left_margin", value = escape(rq.q.getfirst("print_left_margin","").decode("utf8")))
                    LabInfo(name = u"print_report_details", value = escape(rq.q.getfirst("print_report_details","").decode("utf8")))
                    session.commit()
                else:
                    top_margin = LabInfo.get_by(name = u"print_top_margin")
                    top_margin.value = escape(rq.q.getfirst("print_top_margin","").decode("utf8"))
                    bottom_margin = LabInfo.get_by(name = u"print_bottom_margin")
                    bottom_margin.value = escape(rq.q.getfirst("print_bottom_margin","").decode("utf8"))
                    right_margin = LabInfo.get_by(name = u"print_right_margin")
                    right_margin.value = escape(rq.q.getfirst("print_right_margin","").decode("utf8"))
                    left_margin = LabInfo.get_by(name = u"print_left_margin")
                    left_margin.value = escape(rq.q.getfirst("print_left_margin","").decode("utf8"))
                    report_details = LabInfo.get_by(name = u"print_report_details")
                    report_details.value = escape(rq.q.getfirst("print_report_details","").decode("utf8"))
                    session.commit()
                settingsScript = "window.location.replace('%(script)s/page/settings/');" %{'script':rq.script}
        return {'settingsScript':settingsScript, 'script':rq.script}
    @expose(percentTemplate, ['about.html'])
    def about(self, rq, *args):
        return {}
    @expose()
    def the_editor(self, rq, *args):
        return the_editor(rq.script)
    @expose(percentTemplate, ['404.html'], responseCode=404)
    def _404(self, rq, e):
        FileNotFound = "display:none;"
        FileNotFoundFile = "display:none;"
        File = ""
        if rq.uri == None: FileNotFound = ""
        else: FileNotFoundFile = ""; File = rq.uri
        return {'FileNotFound':FileNotFound, 'FileNotFoundFile':FileNotFoundFile, 'File':File, 'script':rq.script}
