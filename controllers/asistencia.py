# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

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
        redirect(URL('view'))
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
        if not form.vars.salida:
            form.vars.salida = datetime.now()

        ## Logica de bonos
        bonos_actuales = db(db.bonos.mascota==form.vars.mascota).select(orderby=~db.bonos.tipo_bono)
        loopmsg = ''
        msg = ''
        for bono in bonos_actuales:
            tipo = bono.tipo_bono.tipo_bono
            loopmsg = loopmsg + "Bono es: " + str(tipo)

            if tipo.find("mes") !=-1 :                                              #Matchea con mes
                if tipo.find("6h")!=-1 :                        #Mes6h
                    if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                        msg = msg + "Bono de mes 6h no valido"
                        #### Siguiente bono
                    else:                                                           #Comprobacion de 6h (valida)
                        if bono.duracion_expira < form.vars.salida.date() :             #Caducidad alcanzada
                            msg = msg + "Bono de mes6h CADUCADO"
                            #### Siguiente bono
                        else:
                            record.bono_usado = tipo                                    #Actualizando DDBB
                            record.caducidad = bono.duracion_expira
                            record.salida = form.vars.salida
                            record.update_record()
                            response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                            redirect(URL('view'))
                            #### Record mes6h
                else:                                                               #Bono de mes validado
                    if bono.duracion_expira < form.vars.salida.date() :             #Caducidad alcanzada
                        msg = msg + "Bono de mes CADUCADO"
                        #### Siguiente bono
                    else:
                        record.bono_usado = tipo                                    #Actualizando DDBB
                        record.caducidad = bono.duracion_expira                     #Comprobacion de mes (valida)
                        record.salida = form.vars.salida
                        record.update_record()
                        response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                        redirect(URL('view'))
                        #### Record mes
            else:
                if tipo.find("10dias") != -1 :                                      #Bono de 10dias
                    if tipo.find("6h")!=-1 :                        #Mes6h
                        if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                            msg = msg + "Bono de 10 dias 6h no valido"
                            #### Siguiente bono
                        else:                                                           #Comprobacion de 6h (valida)
                            if (bono.dias_resto >= 1) :
                                record.bono_usado = tipo                                    #Actualizando DDBB
                                record.caducidad = bono.dias_resto - 1
                                record.salida = form.vars.salida
                                record.update_record()
                                db(db.bonos.id == bono.id).update(dias_resto=record.caducidad)
                                record.update_record()
                                response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                                redirect(URL('view'))
                                #### Record 10dias6h
                            else:
                                msg = msg + "Bono de 10 dias 6h sin dias. Hay que borrar"
                                ### DELETE BONO
                                #### Siguiente bono
                    else:                                                               #Bono de 10dias validado
                        if (bono.dias_resto >= 1) :
                            record.bono_usado = tipo                                    #Actualizando DDBB
                            record.caducidad = bono.dias_resto - 1
                            record.salida = form.vars.salida
                            db(db.bonos.id == bono.id).update(dias_resto=record.caducidad)
                            record.update_record()
                            response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                            redirect(URL('view'))
                            #### Record 10dias
                        else:
                            msg = msg + "Bono de 10 dias 6h sin dias. Hay que borrar"
                            #### Siguiente bono
        msg = msg + "SALIMOS DEL BUCLE SIN BONO"
        msg = msg + "RECORD: " + str(record)
        redirect(URL('view'))
        if not record.caducidad :
            msg = msg + 'No quedan bonos que comprobar'
            record.bono_usado = "dia6h"                                    #Actualizando DDBB
            if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                msg = msg + "Bono de dia suelto"
                record.bono_usado = "dia"                                    #Actualizando DDBB
            record.caducidad = 1
            record.salida = form.vars.salida
            record.update_record()
            response.flash = T("Bono de dia. Asistencia registrada.")
            #### Record 1 dia
            redirect(URL('view'))
    else:
        response.flash = T('Edita información de salida')
        loopmsg = 'No hay bonos'
        msg = 'el codigo pasa por el else'
        bono = 'bono else'
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def view():
    if request.args(0) is None:
        today=datetime(request.now.year,request.now.month,request.now.day)
        rows = db(db.asistencia.entrada>=today).select()
    else:
        rango_asistencia = request.args(0)
        if rango_asistencia=="mes" :
            date_inferior = datetime(request.now.year,request.now.month - 1,request.now.day)
        elif rango_asistencia=="semana":
            date_inferior = datetime(request.now.year,request.now.month,request.now.day - 7)
        elif rango_asistencia=="ayer":
            date_inferior = datetime(request.now.year,request.now.month,request.now.day - 1)
        else:
            date_inferior = datetime(request.now.year,request.now.month,request.now.day)
        rows = db(db.asistencia.entrada>=date_inferior).select()
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def update():
    record = db.asistencia(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.asistencia, record, submit_button='Guardar', deletable = True)
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Bono actualizado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del bono')
    return locals()
