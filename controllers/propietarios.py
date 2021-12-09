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
    form = SQLFORM.factory(Field('nombre_apellidos', label=T('Busqueda por nombre')))
    if request.args(0) is None:
        rows = db(db.propietarios).select()
        if form.process().accepted:
            response.flash = 'Resultados busqueda'
            session.nombre_busqueda = form.vars.nombre
            rows = db(db.propietarios.nombre_apellidos.startswith(session.nombre_busqueda)).select()
        elif form.process().errors:
            response.flash = 'Error en busqueda'
    else:
        nombre = request.args(0)
        rows = db(db.propietarios.nombre_apellidos.startswith(nombre)).select()
    mascotasdir = {}
    for x in rows:
        # selectmascota = db(db.mascotas.propietario==x.id).select(db.mascotas.nombre, '%(nombre)s')
        # mascotasdir[x.id] = selectmascota
        #for cosa in persona.cosa.select(orderby=db.cosa.nombre):
        selectmascotas = db(db.mascotas.propietario==x.id).select(db.mascotas.nombre)
        if len(selectmascotas) != 0:
            mascotasdir[x.id] = selectmascotas[0].nombre
        else:
            mascotasdir[x.id] = ''
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.propietarios(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.propietarios, record)
    if form.process().accepted:
        response.flash = T('Propietario actualizado')
    else:
        response.flash = T('Edita información del propietario')
    return locals()
