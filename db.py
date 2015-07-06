# _*_ coding: UTF-8 _*_
#!/usr/bin/python
"""
MediLab: Small Program for managing Medical Laboratories in Egypt.
"""

from elixir import *

##########################################################################################

#### DATABASE INFORMATION ####
# for mysql engine type: metadata.bind = "mysql://username:password@server/database_name"
# instead of the Next Line (the next line for "SQLite DB" attached with the program).

metadata.bind = "sqlite:///db.sqlite"

#### END OF DATABASE INFORMATION ####

##########################################################################################

#### DON'T CHANGE ANY THING BELOW ####

class LabInfo(Entity):
    """ Main Laboratory Information """
    name = Field(Unicode(20))
    value = Field(UnicodeText)

class members(Entity):
    """ Doctors and Workers Information in the Laboratory """
    username = Field(Unicode(20))
    password = Field(UnicodeText)
    email = Field(Unicode(60))
    phone = Field(Unicode(20))
    is_admin = Field(Integer)
    is_banned = Field(Integer)
    ban_reason = Field(UnicodeText)

class login_attempts(Entity):
    """ Login Attempts from the same ip address that will forbidden after 3 attempts """
    ip_address = Field(Unicode(20))
    attempt_number = Field(Integer(10))
    time = Field(DateTime)

class sessions(Entity):
    """ Session for Login Attempts and Cookies """
    username = Field(Unicode(20))
    is_cookie = Field(Integer)
    time = Field(DateTime)
    session_hash = Field(UnicodeText)

class customers(Entity): 
    """ The Patiants who came to the laboratory to check thier health """
    name = Field(Unicode(100), index=True)
    birth = Field(Date)
    gender = Field(Unicode(10))
    phone = Field(Unicode(20))
    address = Field(UnicodeText)
    notes = Field(UnicodeText)
    bills = OneToMany("bills")
    reports = OneToMany("reports")

class bills(Entity):
    """ bills that contains reports """
    customer = ManyToOne("customers")
    member = ManyToOne("members")
    time = Field(DateTime)
    reports = OneToMany("reports")
    paid = Field(Integer)
    rest = Field(Integer)
    discount = Field(Integer)
    total = Field(Integer)
    notes = Field(UnicodeText)

class reports(Entity):
    """ the results of checking customers """
    title = Field(Unicode(30))
    customer = ManyToOne("customers")
    member = ManyToOne("members")
    bill = ManyToOne("bills")
    content = Field(UnicodeText)
    time = Field(DateTime)
    is_inner = Field(Integer)
    referred_by = Field(Unicode(60))
    price = Field(Integer)
    notes = Field(UnicodeText)
