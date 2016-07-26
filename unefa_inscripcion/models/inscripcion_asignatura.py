# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la Universidad Nacional Experimental
#    Politécnica de la Fuerza Armada, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################
from openerp.osv import fields, osv
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import * 
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re
import random


def filtrar_carreras_regimen_general(self,cr,uid,ids,context=None):
    value={}
    objeto_users=self.pool.get('res.users')
    id_users=objeto_users.search(cr,uid,[('id','=',int(uid))])
    data_users=objeto_users.browse(cr,uid,id_users)
    for name in data_users:
        if name.is_estudiante == True:
            obj_users_estudiante=self.pool.get('unefa.usuario_estudiante')
            id_users_estudiante=obj_users_estudiante.search(cr,uid,[('user_id','=',uid)])
            data_users_estudiante=obj_users_estudiante.browse(cr,uid,id_users_estudiante)
            estudiante = data_users_estudiante['id']
            value={
                'carrera_id':data_users['carrera_id'],
                'user_id':estudiante,
            }
        else:
            if name.is_coordinador == True or name.is_asistente == True:
                value={
                        'carrera_id':data_users['coordinacion_id']['carrera_id'],
                }
    return {'value':value}
    
    
class unefa_inscripcion_asignatura(osv.osv):
    _name='unefa.inscripcion_asignatura'
    _rec_name='user_id'
    
    _columns={ 
        'carrera_id': fields.many2one('unefa.carrera', 'Carrerra', readonly=False,required=True,states={'inscrito': [('readonly', True)]},help='Carrera en la que está inscrito el estudiante', ),
        'user_id': fields.many2one('unefa.usuario_estudiante','Estudiante', readonly=False,required=True,states={'preinscrito': [('readonly', True)],'inscrito': [('readonly', True)]},),
        'fecha_inscripcion':fields.date('Fecha de Inscripción',required=True,readonly=True, help='Fecha de la inscripción de asignaturas actual del estudiante',),
        'periodo_id':fields.many2one('unefa.conf.periodo_academico','Período Académico', required=True,states={'preinscrito': [('readonly', True)],'inscrito': [('readonly', True)]},),
        'asignaturas_inscritas_ids':fields.one2many('unefa.asignatura_inscritas', 'inscripcion_id', 'Asignaturas', states={'inscrito': [('readonly', True)]},required=True,help='Asignaturas relacionadas al pensum'),
        'state':fields.selection([('borrador','Borrador'),('cancelado','Cancelado'),('preinscrito','Preinscrito'),('inscrito','Inscrito')],'Estatus', help='Estatus de la inscripción de asignaturas'),
        'observaciones': fields.text('Observaciones',states={'inscrito': [('readonly', True)]},) ,
        }
    
    _defaults = {
        'active':True,
        'fecha_inscripcion':date.today(),    
        }
    
    _sql_constraints = [
        ('inscripcion_uniq', 'unique(carrera_id,user_id,periodo_id)', 'Ya tiene un registro para éste período académico.')
        ]
    
    _order = 'create_date desc, id desc'
    
    def crear_planilla_inscripcion(self,cr,uid,ids,context=None):
        url='/descargar/planilla_inscripcion/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def preinscribir_asignaturas(self, cr, uid, ids, context=None):
        res_user_obj=self.pool.get('res.users')
        res_user_ids=res_user_obj.search(cr,uid,[('id','=',uid)],context=context)
        res_user_datos=res_user_obj.browse(cr,uid,res_user_ids,context=context)
        if res_user_datos['is_coordinador']==True or res_user_datos['is_asistente']==True:
            carrera_id=res_user_datos['coordinacion_id']['carrera_id']['id']
            turno=res_user_datos['coordinacion_id']['regimen']
        else:
            carrera_id=res_user_datos['carrera_id']['id']
            turno=res_user_datos['regimen']
        
        hoy=date.today()
        for i in self.browse(cr,uid,ids,context=context):
            pensum_id=i.user_id.pensum_id.id
            planificacion_semestre_obj=self.pool.get('unefa.planificacion_semestre')
            planificacion_semestre_ids=planificacion_semestre_obj.search(cr,uid,[('periodo_id','=',int(i.periodo_id)),('carrera_id','=',int(carrera_id)),('turno','=',turno),('state','=','aprobado')])
            planificacion_semestre_datos=planificacion_semestre_obj.browse(cr,uid,planificacion_semestre_ids,context=context)
            if len(planificacion_semestre_ids)==1:
                for p in planificacion_semestre_datos:
                    for a in p.actividad_ids:
                        fecha_desde=datetime.strptime(a.fecha_desde, '%Y-%m-%d')
                        fecha_desde =datetime.date(fecha_desde)
                        fecha_hasta=datetime.strptime(a.fecha_hasta, '%Y-%m-%d')
                        fecha_hasta =datetime.date(fecha_hasta)
                        if res_user_datos['is_coordinador'] != True:
                            if a.actividad_id.actividad=="PREINSCRIPCIÓN":
                                if (cmp(fecha_desde,hoy)==-1 and cmp(hoy,fecha_hasta)==-1) or (cmp(fecha_desde,hoy)==0) or (cmp(hoy,fecha_hasta)==0):
                                    inscripcion_asignatura_obj=self.pool.get('unefa.asignatura_inscritas')
                                    self.validar_inscripcion_horarios(cr,uid,ids,carrera_id,turno)
                                    inscripcion_asignatura_ids=inscripcion_asignatura_obj.search(cr,uid,[('inscripcion_id','=',i.id)],context=context)
                                    inscripcion_asignatura_obj.write(cr,uid,inscripcion_asignatura_ids,{'state':'preinscrito'},context=context)
                                    self.write(cr,uid,ids,{'state':'preinscrito'},0)
                                else:
                                    raise osv.except_osv(
                                                    ('Alerta!'),
                                                    (u'El proceso de preinscricpción no esta habilitado'))
                        else:
                            inscripcion_asignatura_obj=self.pool.get('unefa.asignatura_inscritas')
                            inscripcion_asignatura_ids=inscripcion_asignatura_obj.search(cr,uid,[('inscripcion_id','=',i.id)])
                            self.validar_inscripcion_horarios(cr,uid,ids,carrera_id,turno,pensum_id)
                            inscripcion_asignatura_obj.write(cr,uid,inscripcion_asignatura_ids,{'state':'preinscrito'})
                            self.write(cr,uid,ids,{'state':'preinscrito'},0)
            else:
                raise osv.except_osv(
                        ('Alerta!'),
                        (u'El proceso de preinscricpción no esta habilitado'))
            
        
        return True
    
    def validar_inscripcion_horarios(self,cr,uid,ids,carrera_id,turno,context=None):
        dias_obj=self.pool.get('unefa.horario_dias')
        horarios_obj=self.pool.get('unefa.horarios')
        horarios_seccion_obj=self.pool.get('unefa.horarios_seccion')
        horarios_seccion_datos_obj=self.pool.get('unefa.horarios_seccion_datos')
        list_horas_turno=[]
        list_asignaturas_inscritas=[]
        list_dias=['Lunes','Martes','Miercoles','Jueves','Viernes']
        for records in self.browse(cr,uid,ids):
            periodo_id=records.periodo_id.id
            horarios_id=horarios_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno),('periodo_id','=',periodo_id),])
            horarios_seccion_id=horarios_seccion_obj.search(cr,uid,[('horario_id','in',horarios_id)])
            for asignaturas in records.asignaturas_inscritas_ids:
        
                if asignaturas.inscripcion_especial!=True:
                    list_asignaturas_inscritas.append(asignaturas.asignatura_id.id)
                else:
                    if asignaturas.asignatura_relacion_id.id!=False:
                        list_asignaturas_inscritas.append(asignaturas.asignatura_relacion_id.id)
        list_hora_dia_asignatura=[]
        for dia in list_dias:
            dias_id=dias_obj.search(cr,uid,[('dia','=',dia)])
            horarios_seccion_datos_id=horarios_seccion_datos_obj.search(cr,uid,[('secciones_horario_id','in',horarios_seccion_id),('dia_id','in',dias_id),('asignatura_id','in',list_asignaturas_inscritas),])
            horarios_seccion_datos_data=horarios_seccion_datos_obj.browse(cr,uid,horarios_seccion_datos_id)
            for ho in horarios_seccion_datos_data:
                list_hora_dia_asignatura.append(ho.hora_id.id)
            list_hora_dia_asignatura_f = list(set(list_hora_dia_asignatura))
            if len(list_hora_dia_asignatura_f)!=len(list_hora_dia_asignatura):
                raise osv.except_osv(
                    ('Error!'),
                    (u'Usted esta registrando materias en horario simultaneo el día %s , consulte los horarios')%(dia))
            list_hora_dia_asignatura=[]
        return True
        
    def inscribir_asignaturas(self, cr, uid, ids, context=None):
        res_user_obj=self.pool.get('res.users')
        res_user_ids=res_user_obj.search(cr,uid,[('id','=',uid)],context=context)
        res_user_datos=res_user_obj.browse(cr,uid,res_user_ids,context=context)
        if res_user_datos['is_coordinador']==True or res_user_datos['is_asistente']==True:
            carrera_id=res_user_datos['coordinacion_id']['carrera_id']['id']
            turno=res_user_datos['coordinacion_id']['regimen']
        else:
            carrera_id=res_user_datos['carrera_id']['id']
            turno=res_user_datos['regimen']
        hoy=date.today()
        cantidad_estudiantes_obj=self.pool.get('unefa.cantidad_estudiantes')
        asignatura_inscritas_obj=self.pool.get('unefa.asignatura_inscritas')
        for i in self.browse(cr,uid,ids,context=context):
            for asignatura in i.asignaturas_inscritas_ids:
                if asignatura.inscripcion_especial==True:
                    carrera_id=i.user_id.carrera_id.id
                    turno=i.user_id.regimen
                    cantidad_estudiantes_id=cantidad_estudiantes_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno)])
                    cantidad_estudiantes_data=cantidad_estudiantes_obj.browse(cr,uid,cantidad_estudiantes_id)
                    cantidad_maxima=cantidad_estudiantes_data['cantidad_maxima']
                    asignatura_inscritas_ids=asignatura_inscritas_obj.search(cr,uid,[('seccion_id','=',asignatura.seccion_id.id),('asignatura_id','=',asignatura.asignatura_id.id)])
                    asignatura_inscritas_especial_ids=asignatura_inscritas_obj.search(cr,uid,[('seccion_id','=',asignatura.seccion_id.id),('asignatura_relacion_id','=',asignatura.asignatura_id.id),('state','=','inscrito')])
                    list_alumnos=list(set(asignatura_inscritas_ids) | set(asignatura_inscritas_especial_ids))
                    if len(list_alumnos)>cantidad_maxima:
                         raise osv.except_osv(
                            ('Atención, Ha excedido el límite de alumnos para una sección!'),
                            (u'La seccion %s no tiene cupos habilitados para inscripción en la asignatura %s.')%(asignatura.seccion_id.seccion,asignatura.asignatura_id.asignatura))
            planificacion_semestre_obj=self.pool.get('unefa.planificacion_semestre')
            planificacion_semestre_ids=planificacion_semestre_obj.search(cr,uid,[('periodo_id','=',int(i.periodo_id)),('carrera_id','=',int(carrera_id)),('turno','=',turno),('state','=','aprobado')])
            planificacion_semestre_datos=planificacion_semestre_obj.browse(cr,uid,planificacion_semestre_ids,context=context)
            if len(planificacion_semestre_ids)==1:
                for p in planificacion_semestre_datos:
                    for a in p.actividad_ids:
                        fecha_desde=datetime.strptime(a.fecha_desde, '%Y-%m-%d')
                        fecha_desde =datetime.date(fecha_desde)
                        fecha_hasta=datetime.strptime(a.fecha_hasta, '%Y-%m-%d')
                        fecha_hasta =datetime.date(fecha_hasta)
                        if res_user_datos['is_coordinador'] != True:
                            if a.actividad_id.actividad=="INSCRIPCIÓN":
                                if (cmp(fecha_desde,hoy)==-1 and cmp(hoy,fecha_hasta)==-1) or (cmp(fecha_desde,hoy)==0) or (cmp(hoy,fecha_hasta)==0):
                                    inscripcion_asignatura_obj=self.pool.get('unefa.asignatura_inscritas')
                                    self.validar_prelacion_asignatura(cr,uid,ids)
                                    self.validar_inscripcion_horarios(cr,uid,ids,carrera_id,turno)
                                    self.validar_inscripcion_asignatura_aprobadas(cr,uid,ids)
                                    inscripcion_asignatura_ids=inscripcion_asignatura_obj.search(cr,uid,[('inscripcion_id','=',i.id)],context=context)
                                    inscripcion_asignatura_obj.write(cr,uid,inscripcion_asignatura_ids,{'state':'inscrito'},context=context)
                                    self.write(cr,uid,ids,{'state':'inscrito'},0)
                                else:
                                    raise osv.except_osv(
                                                    ('Alerta!'),
                                                    (u'El proceso de inscripción no esta habilitado'))
                        else:
                            inscripcion_asignatura_obj=self.pool.get('unefa.asignatura_inscritas')
                            self.validar_inscripcion_horarios(cr,uid,ids,carrera_id,turno)
                            self.validar_prelacion_asignatura(cr,uid,ids)
                            self.validar_inscripcion_asignatura_aprobadas(cr,uid,ids)
                            inscripcion_asignatura_ids=inscripcion_asignatura_obj.search(cr,uid,[('inscripcion_id','=',i.id)])
                            inscripcion_asignatura_obj.write(cr,uid,inscripcion_asignatura_ids,{'state':'inscrito'})
                            self.write(cr,uid,ids,{'state':'inscrito'},0)
            else:
                raise osv.except_osv(
                        ('Alerta!'),
                        (u'El proceso de inscripción no esta habilitado'))
        return True
    
    def validar_prelacion_asignatura(self,cr,uid,ids,context=None):
        gestion_semestre_obj=self.pool.get('unefa.gestion_semestre')
        list_periodo_ids=[]
        list_validacion=[]
        for registros in self.browse(cr,uid,ids):
            pensum_id=registros.user_id.pensum_id.id
            estudiante_id=registros.user_id.id
            inscripcion_ids=self.search(cr,uid,[('user_id','=',registros.user_id.id)])
            inscripcion_data=self.browse(cr,uid,inscripcion_ids)
            for periodos in inscripcion_data:
                list_periodo_ids.append(periodos.periodo_id.id)
            for asignatura in registros.asignaturas_inscritas_ids:
                if len(asignatura.asignatura_id.asignaturas_ids)>0:
                    for prelacion in asignatura.asignatura_id.asignaturas_ids:
                        gestion_semestre_ids=gestion_semestre_obj.search(cr,uid,[('asignatura_id','=',prelacion.id),('periodo_id','in',list_periodo_ids)])
                        gestion_semestre_data=gestion_semestre_obj.browse(cr,uid,gestion_semestre_ids)
                        for gestion in gestion_semestre_data:
                            for pensum in gestion.actas_ids:
                                if pensum.pensum_id.id==pensum_id:
                                    for notas in pensum.notas_ids:
                                        if notas.estudiante_id.id==estudiante_id:
                                            if int(notas.definitiva)>=10:
                                                list_validacion.append(notas.id)
                                            else:
                                                for pensumr in gestion.actas_recuperacion_ids:
                                                    if pensumr.pensum_id.id==pensum_id:
                                                        for notasr in pensumr.notas_ids:
                                                            if notasr.estudiante_id.id==estudiante_id:
                                                                if notasr.calificacion!='NP':
                                                                    if int(notasr.calificacion)>=10:
                                                                        list_validacion.append(notasr.id)
                    if len(list_validacion) != len (asignatura.asignatura_id.asignaturas_ids):
                        raise osv.except_osv(
                                ('Alerta!'),
                                (u'Esta intentando inscribir una asignatura que se encuentra prelada.'))
        return True
        
    def validar_inscripcion_asignatura_aprobadas(self,cr,uid,ids,context=None):
        gestion_semestre_obj=self.pool.get('unefa.gestion_semestre')
        list_periodo_ids=[]
        list_validacion=[]
        for registros in self.browse(cr,uid,ids):
            pensum_id=registros.user_id.pensum_id.id
            estudiante_id=registros.user_id.id
            inscripcion_ids=self.search(cr,uid,[('user_id','=',registros.user_id.id)])
            inscripcion_data=self.browse(cr,uid,inscripcion_ids)
            for periodos in inscripcion_data:
                list_periodo_ids.append(periodos.periodo_id.id)
            for asignatura in registros.asignaturas_inscritas_ids:
                gestion_semestre_ids=gestion_semestre_obj.search(cr,uid,[('asignatura_id','=',asignatura.asignatura_id.id),('periodo_id','in',list_periodo_ids)])
                if len(gestion_semestre_ids)!=0:
                    gestion_semestre_data=gestion_semestre_obj.browse(cr,uid,gestion_semestre_ids)
                    for gestion in gestion_semestre_data:
                        for pensum in gestion.actas_ids:
                            if pensum.pensum_id.id==pensum_id:
                                for notas in pensum.notas_ids:
                                    if notas.estudiante_id.id==estudiante_id:
                                        if int(notas.definitiva)>=10:
                                            raise osv.except_osv(
                                                ('Alerta!'),
                                                (u'Esta intentando inscribir una asignatura aprobada.'))
                                        else:
                                            for pensumr in gestion.actas_recuperacion_ids:
                                                if pensumr.pensum_id.id==pensum_id:
                                                    for notasr in pensumr.notas_ids:
                                                        if notasr.estudiante_id.id==estudiante_id:
                                                            if notasr.calificacion!='NP':
                                                                if int(notasr.calificacion)>=10:
                                                                    raise osv.except_osv(
                                                                        ('Alerta!'),
                                                                        (u'Esta intentando inscribir una asignatura aprobada.'))
        return True
    
    def filtrar_carreras_regimen(self,cr,uid,ids,context=None):
        return filtrar_carreras_regimen_general(self,cr,uid,ids)
    
    def validar_asignatura_create(self,cr,uid,ids,asignaturas_ids,carrera,turno,context=None):
        list_uc = []
        list_asignatura_ids = []
        unidades_credito_obj=self.pool.get('unefa.cantidad_unidades_credito')
        
        unidades_credito_ids=unidades_credito_obj.search(cr,uid,[('carrera_id','=',carrera),('turno','=',turno)])
        unidades_credito_data=unidades_credito_obj.browse(cr,uid,unidades_credito_ids)
        
        if asignaturas_ids == []:
            raise osv.except_osv(
                ('Atención!'),
                (u'Seleccione las asignaturas a inscribir, no puede ser vacío.'))
        asignatura_obj=self.pool .get('unefa.asignatura')
        for uc in asignaturas_ids:
            asignatura_data=asignatura_obj.browse(cr,uid,uc[2]['asignatura_id'])
            list_asignatura_ids.append(uc[2]['asignatura_id'])
            list_uc.append(asignatura_data['unidad_credito'])
        sum=0
        for suma in range(0,len(list_uc)):
            sum=sum+list_uc[suma]
    
        if sum > int(unidades_credito_data['cantidad_uc']):
            raise osv.except_osv(
                ('Atención, Ha excedido el límite!'),
                (u'Solo puede agregar hasta un máximo de %s Unidades de crédito.' % (unidades_credito_data['cantidad_uc'])))
        list_asignatura_ids_filtrado=list(set(list_asignatura_ids))
        if len(list_asignatura_ids_filtrado) != len(list_asignatura_ids):
            raise osv.except_osv(
                ('Atención!'),
                (u'Ha selecionado una asigantura dos o más veces.'))
        return True
    
    def validar_inscripcion_write(self,cr,uid,ids,asignaturas_inscritas_ids,context=None):
        list_uc = []
        list_asignatura = []
        asignaturas_inscritas_obj=self.pool.get('unefa.asignatura_inscritas')
        asignatura_obj=self.pool.get('unefa.asignatura')
       
        unidades_credito_obj=self.pool.get('unefa.cantidad_unidades_credito')
        carrera_id=self.browse(cr,uid,ids)['user_id']['carrera_id']['id']
        
        turno=self.browse(cr,uid,ids)['user_id']['regimen']
        
        unidades_credito_ids=unidades_credito_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno)])
        unidades_credito_data=unidades_credito_obj.browse(cr,uid,unidades_credito_ids)
        
        for asignatura in asignaturas_inscritas_ids:
            if asignatura[0]==0:
                asignatura_data=asignatura_obj.browse(cr,uid,asignatura[2]['asignatura_id'])
                list_uc.append(asignatura_data['unidad_credito'])
                list_asignatura.append(asignatura[2]['asignatura_id'])
            else:
                if asignatura[0]==4:
                    list_uc.append(asignaturas_inscritas_obj.browse(cr,uid,asignatura[1])['unidad_credito'])
                    list_asignatura.append(asignaturas_inscritas_obj.browse(cr,uid,asignatura[1])['asignatura_id']['id'])
                else:
                    if asignatura[0]==1:
                        
                        
                        if 'asignatura_id' in asignatura[2].keys():
                            asignatura_data=asignatura_obj.browse(cr,uid,asignatura[2]['asignatura_id'])
                            list_uc.append(asignatura_data['unidad_credito'])
                            list_asignatura.append(asignatura[2]['asignatura_id'])
                        else:
                            list_asignatura.append(asignaturas_inscritas_obj.browse(cr,uid,asignatura[1])['asignatura_id'].id)
                            list_uc.append(asignaturas_inscritas_obj.browse(cr,uid,asignatura[1])['unidad_credito'])
        sum=0
        for suma in range(0,len(list_uc)):
            sum = sum+list_uc[suma]
        if sum > unidades_credito_data['cantidad_uc']:
            raise osv.except_osv(
                ('Atención, Ha excedido el límite!'),
                (u'Solo puede agregar hasta un máximo de %s Unidades de crédito.' % (unidades_credito_data['cantidad_uc'])))
        if sum == 0:
            raise osv.except_osv(
                ('Atención!'),
                (u'Seleccione las asignaturas a inscribir, no puede ser vacío.'))
        list_asignatura_filtrada = []
        list_asignatura_filtrada = list(set(list_asignatura))
        if len(list_asignatura_filtrada) != len(list_asignatura):
            raise osv.except_osv(
                ('Atención!'),
                (u'Ha selecionado la misma asigantura dos o más veces.'))
        return True
    
    def validar_disponibilidad_seccion(self,cr,uid,ids,vals,context=None):
        seccion_obj=self.pool.get('unefa.oferta_academica_seccion')
        asignatura_obj=self.pool.get('unefa.asignatura')
        asignatura_inscritas_obj=self.pool.get('unefa.asignatura_inscritas')
        estudiantes_obj=self.pool.get('unefa.usuario_estudiante')
        estudiante_ids=estudiantes_obj.search(cr,uid,[('id','=',vals['user_id'])])
        estudiante_data=estudiantes_obj.browse(cr,uid,estudiante_ids)
        carrera_id=estudiante_data['carrera_id'].id
        turno=estudiante_data['regimen']
        cantidad_estudiantes_obj=self.pool.get('unefa.cantidad_estudiantes')
        cantidad_estudiantes_id=cantidad_estudiantes_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno)])
        cantidad_estudiantes_data=cantidad_estudiantes_obj.browse(cr,uid,cantidad_estudiantes_id)
        cantidad_maxima=cantidad_estudiantes_data['cantidad_maxima']
        for registro in vals['asignaturas_inscritas_ids']:
            if 'seccion_id' in registro[2]:
                seccion_id=registro[2]['seccion_id']
                asignatura_id=registro[2]['asignatura_id']
                seccion_data=seccion_obj.browse(cr,uid,seccion_id)
                asignatura_data=asignatura_obj.browse(cr,uid,asignatura_id)
                asignatura_inscritas_ids=asignatura_inscritas_obj.search(cr,uid,[('seccion_id','=',seccion_id),('asignatura_id','=',asignatura_id)])
                asignatura_inscritas_especial_ids=asignatura_inscritas_obj.search(cr,uid,[('seccion_id','=',seccion_id),('asignatura_relacion_id','=',asignatura_id),('state','=','inscrito')])
                list_alumnos=list(set(asignatura_inscritas_ids) | set(asignatura_inscritas_especial_ids))
                if len(list_alumnos)>cantidad_estudiantes_data['cantidad_maxima']:
                     raise osv.except_osv(
                        ('Atención, Ha excedido el límite de alumnos para una sección!'),
                        (u'La seccion %s no tiene cupos habilitados para inscripción en la asignatura %s.')%(seccion_data['seccion'],asignatura_data['asignatura']))
        return True
    
    
        
    def create(self,cr,uid,vals,context=None):
        user_carrera = self.filtrar_carreras_regimen(cr,uid,[])
        carrera_id=user_carrera['value']['carrera_id'].id
        usuario_obj=self.pool.get('res.users')
        usuario_data=usuario_obj.browse(cr,uid,uid)
        
        if usuario_data['is_estudiante']==True:
            vals.update({
            'user_id':user_carrera['value']['user_id'],
            })
            turno=usuario_data['regimen']
        else:
            turno=usuario_data['coordinacion_id']['regimen']
        
        vals.update({
            'state':'borrador',
            'carrera_id': carrera_id,
            })
        validar_asignatura = self.validar_asignatura_create(cr,uid,[],vals['asignaturas_inscritas_ids'],vals['carrera_id'],turno)
        self.validar_disponibilidad_seccion(cr,uid,[],vals)
        
        
        
        
        self.validar_disponibilidad_seccion(cr,uid,[],vals)
        return super(unefa_inscripcion_asignatura,self).create(cr,uid,vals,context=context)
        
    def write(self, cr, uid, ids, vals,interno=None, context=None):
        if interno!=0:
            if 'asignaturas_inscritas_ids' in vals.keys():
                validar_inscripcion = self.validar_inscripcion_write(cr,uid,ids,vals['asignaturas_inscritas_ids'])
        return super(unefa_inscripcion_asignatura, self).write(cr, uid, ids, vals, context=context)
    
    
    
class unefa_asignatura_inscritas(osv.osv):
    _name='unefa.asignatura_inscritas'
    _rec_name=''
    
    _columns={ 
        'inscripcion_id': fields.many2one('unefa.inscripcion_asignatura', 'Asignaturas', required=True,help='Carrera en la que está inscrito el estudiante  ', ),
        'semestre_id': fields.many2one('unefa.semestre', 'Semestre', required=True,states={'borrador': [('readonly', True)],'preinscrito': [('readonly', True)],'inscrito': [('readonly', True)]},help='Semestre ha inscribir.', ),
        'semestre_relacion_id': fields.many2one('unefa.semestre', 'Semestre Relación', required=False,states={'borrador': [('readonly', True)],'preinscrito': [('readonly', True)],'inscrito': [('readonly', True)]},help='Semestre ha inscribir.', ),
        'asignatura_id': fields.many2one('unefa.asignatura', 'Asignaturas', required=True,states={'borrador': [('readonly', True)],'preinscrito': [('readonly', True)],'inscrito': [('readonly', True)]},help='Asignaturas ha inscribir.', ),
        'asignatura_relacion_id': fields.many2one('unefa.asignatura', 'Asignatura Relación', required=False,states={'inscrito': [('readonly', True)]},help='Asignaturas relacionada con la inscrita.', ),
        'seccion_id': fields.many2one('unefa.oferta_academica_seccion', 'Sección', required=False,states={'inscrito': [('readonly', True)]},help='Asignaturas ha inscribir.', ),
        'state':fields.selection([('borrador','Borrador'),('cancelado','Cancelado'),('preinscrito','Preinscrito'),('inscrito','Inscrito')],'Estatus', help='Estatus de la inscripción de asignaturas'),
        'unidad_credito': fields.integer('Unidades de Créditos',  readonly=True, required=True,   help='Unidades de creditos de la Asignatura.'),
        'inscripcion_especial':fields.boolean('Inscripcion Especial')
        }
    
    def inscripcion_especial_default(self,cr,uid,ids,context=None):
        return {'value':{'inscripcion_especial':True}}
    
    def domain_semestre_inscripcion(self,cr,uid,ids,estudiante_id,periodo_id,semestre_id,context=None):
        if not estudiante_id:
            raise osv.except_osv(
                ('Aviso!'),
                (u'Seleccione un Estudiante.'))
        if not periodo_id:
            raise osv.except_osv(
                ('Aviso!'),
                (u'Seleccione un Período Académico.'))
        obj_users=self.pool.get('unefa.usuario_estudiante')
        ids_users=obj_users.search(cr,uid,[('id','=',estudiante_id)])
        data_users=obj_users.browse(cr,uid,ids_users)
        pensum = data_users['pensum_id'].id
        carrera = data_users['carrera_id'].id
        regimen = data_users['regimen']
        obj_oferta=self.pool.get('unefa.oferta_academica')
        ids_oferta=obj_oferta.search(cr,uid,[('periodo_id','=',periodo_id),('carrera_id','=',carrera),('turno','=',regimen)])
        data_oferta=obj_oferta.browse(cr,uid,ids_oferta)
        list_semestre=[]
        list_seccion=[]
        for dato in data_oferta['pensum_ids']:
             if dato.pensum_id.id == pensum:
                 for semestre in dato.semestres_ids:
                    list_semestre.append(semestre.semestre_id.id)
                    if semestre_id:
                        if semestre.semestre_id.id==semestre_id:
                            for seccion in semestre.secciones_ids:
                                list_seccion.append(seccion.id)
        val={'asignatura_id':'','unidad_credito':'','seccion_id':''}
        dominio={'semestre_id': [('id', '=', list(list_semestre))],'seccion_id': [('id', '=', list(list_seccion))]}
        return {'domain':dominio,'value':val}
        
    
        
    def domain_asignatura_inscripcion(self,cr,uid,ids,estudiante_id,periodo_id,semestre_id,seccion_id,context=None):
        obj_users=self.pool.get('unefa.usuario_estudiante')
        ids_users=obj_users.search(cr,uid,[('id','=',estudiante_id)])
        data_users=obj_users.browse(cr,uid,ids_users)
        pensum = data_users['pensum_id'].id
        carrera = data_users['carrera_id'].id
        regimen = data_users['regimen']
        obj_oferta=self.pool.get('unefa.oferta_academica')
        ids_oferta=obj_oferta.search(cr,uid,[('periodo_id','=',periodo_id),('carrera_id','=',carrera),('turno','=',regimen)])
        data_oferta=obj_oferta.browse(cr,uid,ids_oferta)
        list_asignatura=[]
        for dato in data_oferta['pensum_ids']:
             if dato.pensum_id.id == pensum:
                 for semestre in dato.semestres_ids:
                     if semestre.semestre_id.id==semestre_id:
                        for seccion in semestre.secciones_ids:
                            if seccion.id==seccion_id:
                                for asignatura in seccion.asignaturas_ids:
                                    list_asignatura.append(asignatura.asignatura_id.id)
        
        val={'asignatura_id':'','unidad_credito':''}
        dominio={'asignatura_id': [('id', '=', list(list_asignatura))]}
        return {'domain':dominio,'value':val}
    
    def buscar_uc(self,cr,uid,ids,asignatura_id,context=None):
        res = {}
        if asignatura_id:
            obj_asignatura=self.pool.get('unefa.asignatura')
            ids_asignatura=obj_asignatura.search(cr,uid,[('id','=',asignatura_id)])
            data_asignatura=obj_asignatura.browse(cr,uid,ids_asignatura)
            for uc in data_asignatura:
                unidad = uc.unidad_credito
            res = {
                'unidad_credito': unidad,
                    }
        return {'value':res}
    
    def domain_semestre_inscripcion_especial(self,cr,uid,ids,estudiante_id,periodo_id,semestre_id):
        if not estudiante_id:
            raise osv.except_osv(
                ('Aviso!'),
                (u'Seleccione un Estudiante.'))
        if not periodo_id:
            raise osv.except_osv(
                ('Aviso!'),
                (u'Seleccione un Período Académico.'))
        obj_users=self.pool.get('unefa.usuario_estudiante')
        ids_users=obj_users.search(cr,uid,[('id','=',estudiante_id)])
        data_users=obj_users.browse(cr,uid,ids_users)
        pensum = data_users['pensum_id'].id
        carrera = data_users['carrera_id'].id
        regimen = data_users['regimen']
        pensum_obj=self.pool.get('unefa.pensum')
        pensum_ids=pensum_obj.search(cr,uid,[('id','=',pensum)])
        pensum_data=pensum_obj.browse(cr,uid,pensum_ids)
        list_semestre=[]
        list_asignatura=[]
        for p in pensum_data:
            for s in p.semestre_ids:
                list_semestre.append(s.id)
                if semestre_id:
                    if semestre_id==s.id:
                        for a in s.asignaturas_ids:
                            list_asignatura.append(int(a))
        val={'asignatura_id':'','unidad_credito':''}
        dominio={'semestre_id': [('id', '=', list(list_semestre))],'asignatura_id': [('id', '=', list(list_asignatura))]}
        return {'domain':dominio,'value':val}
    
    def domain_semestre2_inscripcion_especial(self,cr,uid,ids,estudiante_id,periodo_id,semestre_relacion_id,context=None):
        obj_users=self.pool.get('unefa.usuario_estudiante')
        ids_users=obj_users.search(cr,uid,[('id','=',estudiante_id)])
        data_users=obj_users.browse(cr,uid,ids_users)
        pensum = data_users['pensum_id'].id
        carrera = data_users['carrera_id'].id
        regimen = data_users['regimen']
        obj_oferta=self.pool.get('unefa.oferta_academica')
        ids_oferta=obj_oferta.search(cr,uid,[('periodo_id','=',periodo_id),('carrera_id','=',carrera),('turno','=',regimen)])
        data_oferta=obj_oferta.browse(cr,uid,ids_oferta)
        list_semestre=[]
        list_seccion=[]
        for dato in data_oferta['pensum_ids']:
            for semestre in dato.semestres_ids:
                list_semestre.append(semestre.semestre_id.id)
                if semestre_relacion_id:
                    if semestre.semestre_id.id==semestre_relacion_id:
                        for seccion in semestre.secciones_ids:
                            list_seccion.append(seccion.id)
        val={'asignatura_relacion_id':'','seccion_id':''}
        dominio={'semestre_relacion_id': [('id', '=', list(list_semestre))],'seccion_id': [('id', '=', list(list_seccion))]}
        return {'domain':dominio,'value':val}
    
    def domain_asignatura_inscripcion_especial(self,cr,uid,ids,estudiante_id,periodo_id,seccion_id,context=None):
        obj_seccion=self.pool.get('unefa.oferta_academica_seccion')
        ids_seccion=obj_seccion.search(cr,uid,[('id','=',seccion_id)])
        data_seccion=obj_seccion.browse(cr,uid,ids_seccion)
        list_asignatura=[]
        
        for seccion in data_seccion:
            for asignatura in seccion.asignaturas_ids:
                list_asignatura.append(asignatura.asignatura_id.id)
        
        val={'asignatura_relacion_id':''}
        dominio={'asignatura_relacion_id': [('id', '=', list(list_asignatura))]}
        return {'domain':dominio,'value':val}
    
    
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'borrador',
            'unidad_credito':self.buscar_uc(cr,uid,[],vals['asignatura_id'])['value'].values()[0],
            })
        return super(unefa_asignatura_inscritas,self).create(cr,uid,vals,context=context)
        
        
