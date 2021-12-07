# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from mascotas.py")

def data():
    rows = db(db.mascota).select()
    return locals()

def add():
    form = SQLFORM(db.mascota).process()
    return locals()

def view():
    mascota = ''
    if request.args(0) is None:
        rows = db(db.mascota).select()
    elif request.post_vars:
        mascota = request.post_vars.mascota
        rows = db(db.mascota.perro.startswith(mascota)).select()
    else:
        mascota = request.args(0)
        rows = db(db.mascota.perro.startswith(mascota)).select()
    return locals()

def update():
    record = db.mascota(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.mascota, record)
    if form.process().accepted:
        response.flash = T('Mascota actualizada')
    else:
        response.flash = T('Por favor, completa el formulario de mascota.')
    return locals()