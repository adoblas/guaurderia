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
def validar_salida():
    record = db.asistencia(request.args(0)) or redirect(URL('view'))
    form = SQLFORM(db.asistencia, record, showid=False,
    buttons = [BUTTON('Volver', _type="button", _onClick="parent.location='%s'" % URL('view')), BUTTON('Validar bonos', _type="submit")],
    fields=['salida'])
    hoy = datetime.now().date()
    now = datetime.now()
    dict_bonos = db(db.bonos.mascota==record.mascota).select()
    info = 'Esta es la variable info'
    bono_matcheado = False
    asistencia_output = record
    if form.validate():
        if not form.vars.salida:
            form.vars.salida = now
        ## Logica de bonos
        bonos_actuales = db(db.bonos.mascota==record.mascota).select(orderby=db.bonos.tipo_bono)
        for bono in bonos_actuales:
            while (not bono_matcheado) :
                tipo = bono.tipo_bono.tipo_bono
                if bono.duracion_expira >= form.vars.salida.date() :                         #Comprobacion caducidad
                    if tipo.find("mes") != -1 :                                              #Matchea con mes
                        if tipo.find("6h")!= -1 :                                            #Mes6h
                            if (form.vars.salida - record.entrada) < timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                                info += "Llamamos con:"
                                info += str(bono.tipo_bono.tipo_bono)
                                asistencia_output = bono_validado(record, bono, 1, form.vars.salida, False)
                                bono_matcheado = True
                                info += "Salida de metodo aux: " + str(asistencia_output)
                                response.flash = T('Bono calculado')
                                #### Record mes6h
                        else:                                                               #Bono de mes validado
                            info += "Llamamos con:"
                            info += str(bono.tipo_bono.tipo_bono)
                            asistencia_output = bono_validado(record, bono, 2, form.vars.salida, False)
                            bono_matcheado = True
                            info += "Salida de metodo aux: " + str(asistencia_output)
                            response.flash = T('Bono calculado')
                            #### Record mes
                    else:
                        if tipo.find("10dias") != -1 :                                      #Bono de 10dias
                            if tipo.find("6h")!=-1 :                                        #10dias6h
                                if (form.vars.salida - record.entrada) < timedelta(hours=6) :   #Comprobacion de 6h
                                    if (bono.dias_resto >= 1) :
                                        info += "Llamamos con:"
                                        info += str(bono.tipo_bono.tipo_bono)
                                        asistencia_output = bono_validado(record, bono, 3, form.vars.salida, False)
                                        bono_matcheado = True
                                        info += "Salida de metodo aux: " + str(asistencia_output)
                                        response.flash = T('Bono calculado')
                                        #### Record 10dias6h
                            else:                                                               #Bono de 10dias validado
                                if (bono.dias_resto >= 1) :
                                    info += "Llamamos con:"
                                    info += str(bono.tipo_bono.tipo_bono)
                                    asistencia_output = bono_validado(record, bono, 4, form.vars.salida, False)
                                    bono_matcheado = True
                                    info += "Salida de metodo aux: " + str(asistencia_output)
                                    response.flash = T('Bono calculado')
                                    #### Record 10dias
            if bono_matcheado == False :
                if (form.vars.salida - record.entrada) > timedelta(hours=6) :   #Comprobacion de 6h (excedido)
                    info += "Llamamos con:"
                    info += str(bono.tipo_bono.tipo_bono)
                    asistencia_output = bono_validado(record, '', 5, form.vars.salida, False)
                    info += "Salida de metodo aux: " + str(asistencia_output)
                    response.flash = T('Bono calculado')
                else:
                    info += "Llamamos con:"
                    info += str(bono.tipo_bono.tipo_bono)
                    asistencia_output = bono_validado(record, '', 6, form.vars.salida, False)
                    info += "Salida de metodo aux: " + str(asistencia_output)
                    response.flash = T('Bono calculado')
        bono_matcheado = True
    else:
        response.flash = T('Edita información de salida')
    
    return locals()

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def bono_validado(asistencia, bono, tipo, salida, upload) :
    #info = "La info del bono que llega es:" + '\n'.join(asistencia)
    if (bono == '') : #Bonos de dias sueltos
        bono = db.bonos.insert(mascota=asistencia.mascota, tipo_bono=tipo, duracion_expira=datetime.now().date(), dias_resto=0)

    if (tipo == 1 or tipo == 2) : #Bono de mes
        asistencia.bono_usado = bono                                    #Actualizando DDBB
        asistencia.por_consumir = '-'
        asistencia.caducidad = bono.duracion_expira
        #asistencia.salida = salida
    elif (tipo == 3 or tipo == 4) : #Bono de 10 dias
        asistencia.bono_usado = bono                                    #Actualizando DDBB
        asistencia.por_consumir = bono.dias_resto - 1
        asistencia.caducidad = bono.duracion_expira
        if upload :
            db(db.bonos.id == bono.id).update(dias_resto=asistencia.por_consumir)
    elif (tipo == 5 or tipo == 6) : #Bono de dia suelto
        asistencia.bono_usado = bono
        asistencia.por_consumir = 0
        asistencia.caducidad = datetime.now().date()
    asistencia.salida = salida
    if upload :
        asistencia.salida = datetime.strptime(salida, '%Y-%m-%d_%H_%M_%S.%f')
        asistencia.update_record()
    return asistencia

@auth.requires(lambda: auth.has_membership('employee') or auth.has_membership('admin'))
def registrar():
    asistencia = db.asistencia(request.args(0))
    bono = db.bonos(request.args(1))
    salida = request.args(2)
    bono_validado(asistencia, bono, int(bono.tipo_bono), salida, True)
    redirect(URL('view'))
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
