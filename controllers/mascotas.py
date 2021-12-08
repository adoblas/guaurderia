# -*- coding: utf-8 -*-
def index(): return dict(message="hello from mascotass.py")

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def data():
    rows = db(db.mascotas).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.mascotas).process()
    if form.process().accepted:
        response.flash = T('Mascota creada')
        redirect(URL('view'))
    else:
        response.flash = T('Error al crear mascota. Revisa el formulario.')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    form = SQLFORM.factory(Field('nombre'))
    if request.args(0) is None:
        rows = db(db.mascotas).select()
        if form.process().accepted:
            response.flash = 'Resultados busqueda'
            session.nombre_busqueda = form.vars.nombre
            rows = db(db.mascotas.nombre.startswith(session.nombre_busqueda)).select()
        elif form.process().errors:
            response.flash = 'Error en busqueda'
    else:
        nombre = request.args(0)
        rows = db(db.mascotas.nombre.startswith(nombre)).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.mascotas(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.mascotas, record)
    if form.process().accepted:
        response.flash = T('Mascotas actualizada')
    else:
        response.flash = T('Por favor, completa el formulario de mascotas.')
    return locals()
