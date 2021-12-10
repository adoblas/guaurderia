# -*- coding: utf-8 -*-
def index(): #return dict(message="hello from propietarios.py")
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def data():
    rows = db(db.propietarios).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.propietarios).process()
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Propietario creado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del nuevo propietario')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    form = SQLFORM.factory(
        Field('nombre_busqueda', label=T('Buscar propietario')), 
        submit_button='Buscar')
    if form.process().accepted:
        response.flash = 'Resultados busqueda'
        session.nombrebusqueda = form.vars.nombre_busqueda
        if not session.nombrebusqueda:
            rows = db(db.propietarios).select(limitby=(0, 50))
        else:    
            rows = db(db.propietarios.nombre_apellidos.contains(session.nombrebusqueda)).select()
    else:
        if request.args(0) is None:
            rows = db(db.propietarios).select(limitby=(0, 50))
        else:
            nombre = request.args(0)
            if nombre.find("-") == -1:
                rows = db(db.propietarios.nombre_apellidos.startswith(nombre)).select()
                form.add_button('Volver', URL('view'))
            else:
                listarango = nombre.split('-')
                rango_inf = listarango[0]
                rango_sup = listarango[1]
                rows = db(db.propietarios).select(limitby=(int(rango_inf), int(rango_sup)))
    mascotasdir = {}
    for x in rows:
        selectmascotas = db(db.mascotas.propietario==x.id).select(db.mascotas.nombre,db.mascotas.id)
        if len(selectmascotas) != 0:
            mascotadata = []
            mascotadata.append(selectmascotas[0].id)
            mascotadata.append(selectmascotas[0].nombre)
            mascotasdir[x.id] = mascotadata
        else:
            mascotasdir[x.id] = ['','']
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.propietarios(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.propietarios, record, submit_button='Guardar')
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Propietario actualizado')
    else:
        response.flash = T('Edita información del propietario')
    return locals()
