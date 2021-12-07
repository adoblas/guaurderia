# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from blog.py")

def post():
    form = SQLFORM(db.blog).process()
    return locals()

def view():
    rows = db(db.blog).select(orderby=~db.blog.id)
    return locals()

def display_form():
    form = SQLFORM(db.blog)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('thanks'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return locals()

def update():
    record = db.blog(request.args(0)) or redirect(URL('post'))
    form = SQLFORM(db.blog, record)
    if form.process().accepted:
        response.flash = T('Entry updated in DB')
    else:
        response.flash = T('Please complete the form')
    return locals()

def thanks():
    return locals()
