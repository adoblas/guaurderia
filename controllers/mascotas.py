# -*- coding: utf-8 -*-
def index():
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def data():
    rows = db(db.mascotas).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.mascotas).process()
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Mascota creada')
        redirect(URL('view'))
    else:
        response.flash = T('Edita la información del nuevo peludo.')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    form = SQLFORM.factory(
        Field('nombre_busqueda', label=T('Buscar mascota')), 
        submit_button='Buscar')
    if form.process().accepted:
        response.flash = 'Resultados busqueda'
        session.nombrebusqueda = form.vars.nombre_busqueda
        if not session.nombrebusqueda:
            rows = db(db.mascotas).select(limitby=(0, 50))
        else:    
            rows = db(db.mascotas.nombre.contains(session.nombrebusqueda)).select()
    else:
        if request.args(0) is None:
            rows = db(db.mascotas).select(limitby=(0, 50))
        else:
            nombre = request.args(0)
            if nombre.find("-") == -1:
                rows = db(db.mascotas.nombre.startswith(nombre)).select()
                form.add_button('Volver', URL('view'))
            else:
                listarango = nombre.split('-')
                rango_inf = listarango[0]
                rango_sup = listarango[1]
                rows = db(db.mascotas).select(limitby=(int(rango_inf), int(rango_sup)))
    bonosdir = {}
    for x in rows:
        selectbonos = db(db.bonos.mascota==x.id).select(db.bonos.tipo_bono,db.bonos.id)
        if len(selectbonos) != 0:
            bonodata = []
            bonodata.append(selectbonos[0].id)
            bonodata.append(selectbonos[0].tipo_bono)
            bonosdir[x.id] = bonodata
        else:
            bonosdir[x.id] = ['','']
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.mascotas(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.mascotas, record, submit_button='Guardar')
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Macota actualizada')
    else:
        response.flash = T('Edita información del peludo')
    return locals()
