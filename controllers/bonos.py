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
    if form.process().accepted:
        response.flash = T('Bono creado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del nuevo bono')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    hoy = datetime.now().date()
    if request.args(0) is None:
        rows = db(db.bonos).select(limitby=(0, 50))
    else:
        tipo = request.args(0)
        if tipo == 'caducados' :
            # Bonos caducados
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