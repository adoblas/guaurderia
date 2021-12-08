# -*- coding: utf-8 -*-
# intente algo como
def index(): return dict(message="hello from propietarios.py")

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def data():
    rows = db(db.propietarios).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.propietarios).process()
    if form.process().accepted:
        response.flash = T('Propietario creado')
        redirect(URL('view'))
    else:
        response.flash = T('Error al crear propietario. Revisa el formulario.')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    form = SQLFORM.factory(Field('nombre'))
    if request.args(0) is None:
        rows = db(db.propietarios).select()
        if form.process().accepted:
            response.flash = 'Resultados busqueda'
            session.nombre_busqueda = form.vars.nombre
            rows = db(db.propietarios.nombre.startswith(session.nombre_busqueda)).select()
        elif form.process().errors:
            response.flash = 'Error en busqueda'
    else:
        nombre = request.args(0)
        rows = db(db.propietarios.nombre.startswith(nombre)).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.propietarios(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.propietarios, record)
    if form.process().accepted:
        response.flash = T('Propietario actualizado')
    else:
        response.flash = T('Por favor, completa el formulario de propietarios.')
    return locals()
