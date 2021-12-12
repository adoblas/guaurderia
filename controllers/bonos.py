# -*- coding: utf-8 -*-
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
