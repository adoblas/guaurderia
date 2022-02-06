# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

import logging
logger = logging.getLogger("web2py.app.myweb2pyapplication")
logger.setLevel(logging.DEBUG)

def index():
    redirect(URL('view'))
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def add():
    form = SQLFORM(db.asistencia,
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Registrar entrada', _type="submit")],
    fields=['mascota', 'entrada'])
    if not form.vars.entrada:
        form.vars.entrada = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if form.process().accepted:
        #response.flash = T('Entrada registrada')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del nuevo bono')
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def salida():
    record = db.asistencia(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.asistencia, record, showid=False,
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Registrar salida', _type="submit")],
    fields=['salida'])
    hoy = datetime.now().date()
    dict_bonos = db(db.bonos.mascota==record.mascota).select()
    if form.validate():
        if not form.vars.salida:
            form.vars.salida = datetime.now()

        ## Logica de bonos
        bonos_actuales = db(db.bonos.mascota==record.mascota).select(orderby=db.bonos.tipo_bono)
        msg = ''
        for bono in bonos_actuales:
            tipo = bono.tipo_bono.tipo_bono
            
            if bono.duracion_expira < form.vars.salida.date() :   #Comprobacion de 6h (excedido)
                msg = msg + "\nBono caducado"
                #### Siguiente bono
            else:
                if tipo.find("mes") !=-1 :                                              #Matchea con mes
                    if tipo.find("6h")!=-1 :                                            #Mes6h
                        if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                            msg = msg + "\nBono de mes 6h no valido"
                            #### Siguiente bono
                        else:                                                           #Comprobacion de 6h (valida)
                            record.bono_usado = bono                                    #Actualizando DDBB
                            record.caducidad = bono.duracion_expira
                            record.por_consumir = '-'
                            record.salida = form.vars.salida
                            record.update_record()
                            msg = msg + "\nBono elegido =====> " + tipo
                            response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                            redirect(URL('view'))
                            #### Record mes6h
                    else:                                                               #Bono de mes validado
                        record.bono_usado = bono                                    #Actualizando DDBB
                        record.caducidad = bono.duracion_expira                     #Comprobacion de mes (valida)
                        record.por_consumir = '-'
                        record.salida = form.vars.salida
                        record.update_record()
                        msg = msg + "\nBono elegido =====> " + tipo
                        response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                        redirect(URL('view'))
                        #### Record mes
                else:
                    if tipo.find("10dias") != -1 :                                      #Bono de 10dias
                        if tipo.find("6h")!=-1 :                                        #10dias6h
                            if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                                msg = msg + "\nBono de 10 dias 6h no valido"
                                #### Siguiente bono
                            else:                                                           #Comprobacion de 6h (valida)
                                if (bono.dias_resto >= 1) :
                                    record.bono_usado = bono                                    #Actualizando DDBB
                                    record.caducidad = bono.duracion_expira
                                    record.por_consumir = bono.dias_resto - 1
                                    record.salida = form.vars.salida
                                    record.update_record()
                                    db(db.bonos.id == bono.id).update(dias_resto=record.por_consumir)
                                    record.update_record()
                                    msg = msg + "\nBono elegido =====> " + tipo
                                    response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                                    redirect(URL('view'))
                                    #### Record 10dias6h
                                else:
                                    msg = msg + "\nBono de 10 dias 6h sin dias. Hay que borrar"
                                    ### DELETE BONO
                                    #### Siguiente bono
                        else:                                                               #Bono de 10dias validado
                            if (bono.dias_resto >= 1) :
                                record.bono_usado = bono                                    #Actualizando DDBB
                                record.caducidad = bono.duracion_expira
                                record.por_consumir = bono.dias_resto - 1
                                record.salida = form.vars.salida
                                record.update_record()
                                db(db.bonos.id == bono.id).update(dias_resto=record.por_consumir)
                                record.update_record()
                                msg = msg + "\nBono elegido =====> " + tipo
                                response.flash = T("Bono de 6 horas mes usado. Asistencia registrada.")
                                redirect(URL('view'))
                                #### Record 10dias
                            else:
                                msg = msg + "\nBono de 10 dias 6h sin dias. Hay que borrar"
                                #### Siguiente bono
        msg = msg + "\nSALIMOS DEL BUCLE SIN BONO"
        msg = msg + "\nBONOS: " + str(bonos_actuales)
        msg = msg + "\nRECORD: " + str(record)
       ## Bono de día
        if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
            newBono = db.bonos.insert(mascota=record.mascota, tipo_bono=6, duracion_expira=datetime.now().date(), dias_resto=0)
            record.bono_usado = newBono
            msg = msg + "\nBono de dia suelto"
            #### Record 1 dia
        else :
            newBono = db.bonos.insert(mascota=record.mascota, tipo_bono=5, duracion_expira=datetime.now().date(), dias_resto=0)
            record.bono_usado = newBono
            msg = msg + "\nBono de dia suelto 6h"
            record.bono_usado = newBono
        record.caducidad = datetime.now().date()
        record.por_consumir = 0
        record.salida = form.vars.salida
        record.update_record()
        response.flash = T("Bono de dia. Asistencia registrada.")
        redirect(URL('view'))
        #### Record 1 dia 6h
    else:
        response.flash = T('Edita información de salida')
        msg = ''
        bono = ''
        newBono = ''
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
    form = SQLFORM(db.asistencia, record, showid=False, submit_button='Guardar', deletable = True)
    form.add_button('Volver', URL('view'))
    if form.process().accepted:
        response.flash = T('Bono actualizado')
        redirect(URL('view'))
    else:
        response.flash = T('Edita información del bono')
    return locals()
