#_*_ coding: UTF-8 _*_
#!/usr/bin/python
# Filename: templates_db.py: the separate templates database.


from elixir import *

metadata.bind = "sqlite:///templates_db.sqlite"

class templates(Entity):
    
    title = Field(Unicode(30))
    price = Field(Integer)
    notes = Field(UnicodeText)
    
class normals(Entity):
    
    gender = Field(Unicode(10))
    from_age = Field(Date)
    to_age = Field(Date)
    content = Field(UnicodeText)
    template = ManyToOne('templates')
