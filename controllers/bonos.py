# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

def index():
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.bonos, 
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Crear bono', _type="submit")]).process()
    if form.accepted:
        redirect(URL('view'))
    elif form.errors:
        response.flash = 'Revisa el formulario. Faltan datos requeridos.'    
    else:
        response.flash = T('Edita información del nuevo bono')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    hoy = datetime.now().date()
    total_bonos = db(db.bonos).count()
    form = SQLFORM.factory(
        Field('nombre_busqueda', label=T('Buscar mascota')), 
        submit_button='Buscar').process()
    if form.accepted:
        response.flash = 'Resultados busqueda'
        session.nombrebusqueda = form.vars.nombre_busqueda
        if not session.nombrebusqueda:
            rows = db(db.bonos).select(limitby=(0, 100))
        else:    
            rows = db(db.bonos).select().find(lambda row: session.nombrebusqueda in row.mascota.nombre)
    else:
        if request.args(0) is None:
            rows = db(db.bonos).select(limitby=(0, 100))
        else:
            tipo = request.args(0)
            if tipo == 'caducados' :
                rows = db(db.bonos.duracion_expira < datetime.now().date()).select()
            elif tipo == 'proximosacaducar' :
                rows = db((db.bonos.duracion_expira < datetime.now().date() + timedelta(days=10))&(db.bonos.duracion_expira >= datetime.now().date())).select()
            else:
                rows = db(db.bonos.tipo_bono==tipo).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.bonos(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.bonos, record, showid=False, submit_button='Guardar', deletable = True)
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Bono actualizado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del bono')
    return locals()
    

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def delete():
    record = db.bonos(request.args(0)) or redirect(URL('view'))
    if record :
        db(db.bonos.id == request.args(0)).delete()
    return locals()