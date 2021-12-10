# -*- coding: utf-8 -*-
def index(): #return dict(message="hello from propietarios.py")
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.propietarios, 
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Crear propietario', _type="submit")]).process()
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
            listarango = nombre.split('-')
            rango_inf = listarango[0]
            rango_sup = listarango[1]
            rows = db(db.propietarios).select(limitby=(int(rango_inf), int(rango_sup)))
    dict_mascotas = {}
    for x in rows:
        dict_mascotas[x.id] = db(db.mascotas.propietario==x.id).select(db.mascotas.nombre,db.mascotas.id)
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.propietarios(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.propietarios, record, deletable = True, 
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Guardar cambios', _type="submit")])
    if form.process().accepted:
        response.flash = T('Propietario actualizado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del propietario')
    return locals()
