# -*- coding: utf-8 -*-
def index():
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.bonos, 
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Crear bono', _type="submit")]).process()
    precio = 0
    if form.process().accepted:
        response.flash = T('Bono creado')
        session.nombrebusqueda = form.vars.nombre_busqueda
        tipo_bono = db(db.tipo_bono.tipo_bono=="mes").select()
        precio = tipo_bono
        #redirect(URL('view'))
    else:
        response.flash = T('Edita información del nuevo bono')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    # form = SQLFORM.factory(
    #     Field('nombre_busqueda', label=T('Buscar bonos')), 
    #     submit_button='Buscar')
    # if form.process().accepted:
    #     response.flash = 'Resultados busqueda'
    #     session.nombrebusqueda = form.vars.nombre_busqueda
    #     if not session.nombrebusqueda:
    #         rows = db(db.bonos).select(limitby=(0, 50))
    #     else:    
    #         rows = db(db.bonos.mascota.nombre.contains(session.nombrebusqueda)).select()
    # else:
    if request.args(0) is None:
        rows = db(db.bonos).select(limitby=(0, 50))
    else:
        tipo = request.args(0)
        rows = db(db.bonos.tipo_bono==tipo).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.bonos(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.bonos, record, submit_button='Guardar', deletable = True)
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Bono actualizado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del bono')
    return locals()
