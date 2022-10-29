# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

def index():
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    form = SQLFORM.factory(
        Field('nombre_busqueda', label=T('Buscar mascota')), 
        submit_button='Buscar').process()
    if form.accepted:
        response.flash = 'Resultados busqueda'
        session.nombrebusqueda = form.vars.nombre_busqueda
        if not session.nombrebusqueda:
            rows = db(db.asistencia).select(limitby=(0, 100))
        else:    
            rows = db(db.asistencia).select(groupby=db.asistencia.mascota).find(lambda row: session.nombrebusqueda in row.mascota.nombre)
    else:
        if request.args(0) is None:
            rows = db(db.asistencia).select(limitby=(0, 100), orderby=db.asistencia.mascota , groupby=db.asistencia.mascota)
        else:
            id_mascota = request.args(0)
            rows = db(db.asistencia.mascota==id_mascota).select()
    dict_bonos = {}
    for x in rows:
        dict_bonos[x.id] = db(db.bonos.mascota==x.mascota).select(db.bonos.tipo_bono,db.bonos.id)
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view_mascota():
    id_mascota = request.args(0)
    rows = db(db.asistencia.mascota==id_mascota).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view_bono():
    id_bono = request.args(0)
    rows = db(db.asistencia.bono_usado==id_bono).select()
    return locals()
