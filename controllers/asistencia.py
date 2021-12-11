# -*- coding: utf-8 -*-
import datetime

def index():
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.asistencia,
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Registrar entrada', _type="submit")],
    fields=['mascota', 'entrada'])
    if form.process().accepted:
        # record = db(db.asistencia).select().last()
        # db.asistencia.insert(mascota=record.mascota, entrada=record.entrada)
        response.flash = T('Entrada registrada')
    else:
        response.flash = T('Edita información del nuevo bono')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def salida():
    record = db.asistencia(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.asistencia, record,
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Registrar salida', _type="submit")],
    fields=['mascota', 'salida'])
    if form.validate():
        ## Logica de bonos
        bonos_actuales = db(db.bonos.mascota==form.vars.mascota).select(orderby=db.bonos.tipo_bono)
        for bono in bonos_actuales:
            if "mes6h" in bono.tipo_bono.tipo_bono : #Comprobacion de mes
                caducidad_bono = datetime.datetime(bono.duracion_expira.year,bono.duracion_expira.month,bono.duracion_expira.day)
                if form.vars.salida > caducidad_bono :
                    #Borrar bono o marcar como invalido
                    msg = "El bono ha caducado"
                else:
                    #compruebo horas
                # record_validado = record
                # record_validado.bono = bono
                # form_validado = SQLFORM(db.bonos, record_validado).process()
                    response.flash = T('Bono actualizado')
        #redirect(URL('view'))
    else:
        response.flash = T('Edita información de salida')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    if request.args(0) is None:
        today=datetime.datetime(request.now.year,request.now.month,request.now.day)
        rows = db(db.asistencia.entrada>=today).select()
    else:
        rango_asistencia = request.args(0)
        if rango_asistencia=="mes" :
            date_inferior = datetime.datetime(request.now.year,request.now.month - 1,request.now.day)
        elif rango_asistencia=="semana":
            date_inferior = datetime.datetime(request.now.year,request.now.month,request.now.day - 7)
        elif rango_asistencia=="ayer":
            date_inferior = datetime.datetime(request.now.year,request.now.month,request.now.day - 1)
        else:
            date_inferior = datetime.datetime(request.now.year,request.now.month,request.now.day)
        rows = db(db.asistencia.entrada>=date_inferior).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.asistencia(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.bonos, record, submit_button='Guardar', deletable = True)
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Bono actualizado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del bono')
    return locals()
