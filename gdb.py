# _*_ coding: UTF-8 _*_
#!/usr/bin/python
"""
MediLab: Small Program for managing Medical Laboratories in Egypt.
"""

from google.appengine.ext import db

class EntityModel(db.Model):
    
    def get_by(self, id):
        return self.get_by_id(id)

class session():
    def commit(self):
        db.put()

class LabInfo(EntityModel):
    
    name = db.StringProperty()
    value = db.TextProperty()
    
class members(EntityModel):
    
    username = db.StringProperty()
    password = db.TextProperty()
    email = db.StringProperty()
    phone = db.StringProperty()
    is_admin = db.IntegerProperty()
    is_banned = db.IntegerProperty()
    ban_reason = db.TextProperty()
    
class sessions(EntityModel):
    
    username = db.StringProperty()
    is_cookie = db.IntegerProperty()
    time = db.DateTimeProperty()
    session_hash = db.TextProperty()

class customers(EntityModel):

    """ The Patiants who came to the laboratory to check thier health """
    name = db.StringProperty()
    birth = db.DateProperty()
    gender = db.StringProperty()
    phone = db.StringProperty()
    address = db.TextProperty()
    notes = db.TextProperty()

class bills(EntityModel):
    """ bills that contains reports """
    customer = db.ReferenceProperty(customers, collection_name = "bills")
    member = db.ReferenceProperty(members, collection_name = "bills")
    time = db.DateTimeProperty()
    paid = db.FloatProperty()
    rest = db.FloatProperty()
    discount = db.FloatProperty()
    total = db.FloatProperty()
    notes = db.TextProperty()

class reports(EntityModel):
    """ the results of checking customers """
    title = db.StringProperty()
    customer = db.ReferenceProperty(customers, collection_name = "reports")
    member = db.ReferenceProperty(members, collection_name = "reports")
    bill = db.ReferenceProperty(bills, collection_name = "reports")
    content = db.TextProperty()
    time = db.DateTimeProperty()
    is_inner = db.IntegerProperty()
    referred_by = db.StringProperty()
    price = db.FloatProperty()
    notes = db.TextProperty()

class templates(EntityModel):
    """ the prepared templates for reports """
    title = db.StringProperty()
    from_age = db.IntegerProperty()
    to_age = db.IntegerProperty()
    content = db.TextProperty()
    price = db.FloatProperty()
    notes = db.TextProperty()
