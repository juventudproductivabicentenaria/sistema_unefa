# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la UNEFA, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import * 
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re

class unefa_horarios(osv.osv):

    _name='unefa.horarios'
    _rec_name="id"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def default_carrera(self, cr, uid, ids, context=None):
        users_obj=self.pool.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)],context=context)
        users_data=users_obj.browse(cr,uid,users_ids)
        return int(users_data['coordinacion_id'].carrera_id)
        
    def default_regimen(self, cr, uid, ids, context=None):
        users_obj=self.pool.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)],context=context)
        users_data=users_obj.browse(cr,uid,users_ids)
        return users_data['coordinacion_id'].regimen
    
    _columns = {
        'carrera_id':fields.many2one('unefa.carrera','Carrera', required=True,readonly=True,),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO'),],'Turno', required=True,readonly=True),
        'state':fields.selection([('borrador','Borrador'),('aprobado','Aprobado'),('publicado','Publicado')],'Estado', required=False,),
        'pensum_id':fields.many2one('unefa.pensum','Pensum', required=True, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'periodo_id':fields.many2one('unefa.conf.periodo_academico','Período Académico', required=True, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'secciones_ids':fields.one2many('unefa.horarios_seccion','horario_id','Sección', required=True,),
        }
    
    _sql_constraints = [
        ('horario_uniq', 'unique(carrera_id,turno,pensum_id,periodo_id)', 'Ya existe un registro para este Período Académico.')
        ]
    _defaults = {
        'carrera_id': default_carrera,
        'turno': default_regimen,
    }
    
    _order = 'create_date desc, id desc'
    
    def aprobar_horario(self,cr,uid,ids,context=None):
        
        list_partners=[]
        mail_message_obj=self.pool.get('mail.message')
        usuarios_obj=self.pool.get('res.users')
        
        for registros in self.browse(cr,uid,ids):
            periodo=registros.periodo_id.periodo_academico
            usuarios_ids=usuarios_obj.search(cr,uid,[('carrera_id','=',registros.carrera_id.id),('regimen','=',registros.turno),('is_profesor','=',True)])
            usuarios_data=usuarios_obj.browse(cr,uid,usuarios_ids)
        for usuario in usuarios_data:
            list_partners.append(usuario.partner_id.id)
        
        values={
            'body': 'Ha sido aprobada el horario de clases para el período '+periodo+'.', 
            'model': 'unefa.horarios', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, list_partners]], 
            'subject': False}
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        
        return self.write(cr,uid,ids,{'state':'aprobado'})
    
    def publicar_horario(self,cr,uid,ids,context=None):
        horarios_seccion=self.pool.get('unefa.horarios_seccion')
        horarios_seccion_ids=horarios_seccion.search(cr,uid,[('horario_id','=',ids[0])])
        horarios_seccion_2_ids=horarios_seccion.search(cr,uid,[('horario_id','=',ids[0]),('creado','=',True)])
        if len(horarios_seccion_ids)!=len(horarios_seccion_2_ids):
            raise osv.except_osv(
                ('Aviso!'),
                (u'Aseurese de crear un horario para todas las secciones.'))  
        for ids_s in horarios_seccion_ids:
            horarios_seccion.write(cr,uid,ids_s,{'state':'publicado'})
        
        list_partners=[]
        mail_message_obj=self.pool.get('mail.message')
        usuarios_obj=self.pool.get('res.users')
        
        for registros in self.browse(cr,uid,ids):
            periodo=registros.periodo_id.periodo_academico
            usuarios_ids=usuarios_obj.search(cr,uid,[('carrera_id','=',registros.carrera_id.id),('regimen','=',registros.turno)])
            usuarios_data=usuarios_obj.browse(cr,uid,usuarios_ids)
        for usuario in usuarios_data:
            list_partners.append(usuario.partner_id.id)
        
        values={
            'body': 'Ha sido publicado el horario de clases para el período '+periodo+'.', 
            'model': 'unefa.horarios', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, list_partners]], 
            'subject': False}
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        
        return self.write(cr,uid,ids,{'state':'publicado'})
        
    def descargar_horarios_principal(self,cr,uid,ids,context=None):
        url='/descargar/horarios/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }

    def limpiar_campos_pensum(self,cr,uid,ids,pensum_id,context=None):
        res={}
        if pensum_id:
            res={
                'periodo_id':'',
                'secciones_ids':'',
                }
        return {'value':res}
        
    def cargar_secciones_default(self,cr,uid,ids,carrera_id,turno,periodo_id,pensum_id,context=None):
        if periodo_id:
            mensaje={
                    'title':('Aviso'),
                    'message':('Seleccione una Carrera, un Turno y un Pensum de Estudio'),
                    }
            if not carrera_id :
                res={'periodo_id':''}
                return {'value':res,'warning':mensaje}
            if not turno :
                res={'periodo_id':''}
                return {'value':res,'warning':mensaje}
            if not pensum_id :
                res={'periodo_id':''}
                return {'value':res,'warning':mensaje}
        user_obj=self.pool.get('res.users')
        user_ids=user_obj.search(cr,uid,[('id','=',uid)])
        user_data=user_obj.browse(cr,uid,user_ids)
        piso_id=user_data['coordinacion_id'].coordinaciones_ids.id
        list_secciones=[]
        oferta_obj=self.pool.get('unefa.oferta_academica')
        oferta_id=oferta_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno),('periodo_id','=',periodo_id)])
        oferta_data=oferta_obj.browse(cr,uid,oferta_id)
        for pensum in oferta_data:
            for semestre in pensum.pensum_ids:
                if pensum_id==semestre.pensum_id.id:
                    for seccion in semestre.semestres_ids:
                        for i in seccion.secciones_ids:
                            list_secciones.append([0,False,{'seccion_id' : i.id,'piso_id':piso_id}])
        res={
            'secciones_ids':list_secciones,
            }
        return {'value':res}
        
        
    def validar_datos_repetidos_create(self,cr,uid,ids,vals,context=None):
        list_seccion=[]
        list_aula=[]
        for i in vals['secciones_ids']:
            if 'seccion_id' in i[2].keys():
                list_seccion.append(i[2]['seccion_id'])
            if 'aula_id' in i[2].keys():
                list_aula.append(i[2]['aula_id'])
       
        list_seccion_filtrada = list(set(list_seccion))
        list_aula_filtrada = list(set(list_aula))
        if len(list_seccion_filtrada)!=len(list_seccion):
            raise osv.except_osv(
                ('Error!'),
                (u'Usted ha seleccionado 2 veces una Sección para un mismo Registro.'))  
        if len(list_aula_filtrada)!=len(list_aula):
            raise osv.except_osv(
                ('Error!'),
                (u'Usted ha seleccionado 2 veces una misma aula para dos secciones diferentes.'))  
        return True   
        
    def validar_datos_repetidos_write(self,cr,uid,ids,vals,context=None):
        list_seccion=[]
        list_aula=[]
        seccion_horario=self.pool.get('unefa.horarios_seccion')
        for i in vals['secciones_ids']:
            if i[0]==4:
                list_seccion.append(seccion_horario.browse(cr,uid,i[1])['seccion_id']['id'])
                list_aula.append(seccion_horario.browse(cr,uid,i[1])['aula_id']['id'])
            if i[0]==0:
                if 'seccion_id' in i[2].keys():
                    list_seccion.append(i[2]['seccion_id'])
                if 'aula_id' in i[2].keys():
                    list_aula.append(i[2]['aula_id'])
            if i[0]==1:
                if 'seccion_id' in i[2].keys():
                    list_seccion.append(i[2]['seccion_id'])
                else:
                    list_seccion.append(seccion_horario.browse(cr,uid,i[1])['seccion_id']['id'])
                if 'aula_id' in i[2].keys():
                    list_aula.append(i[2]['aula_id'])
                else:
                    list_aula.append(seccion_horario.browse(cr,uid,i[1])['aula_id']['id'])
        list_seccion_filtrada = list(set(list_seccion))
        list_aula_filtrada = list(set(list_aula))
        if len(list_seccion_filtrada)!=len(list_seccion):
            raise osv.except_osv(
                ('Error!'),
                (u'Usted ha seleccionado 2 veces una Sección para un mismo Registro.'))  
        if len(list_aula_filtrada)!=len(list_aula):
            raise osv.except_osv(
                ('Error!'),
                (u'Usted ha seleccionado 2 veces una misma aula para dos secciones diferentes.'))  
        return True   
            
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        self.validar_datos_repetidos_create(cr,uid,[],vals)
        return super(unefa_horarios,self).create(cr,uid,vals,context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'secciones_ids' in vals.keys():
            self.validar_datos_repetidos_write(cr,uid,[],vals)
        return super(unefa_horarios, self).write(cr, uid, ids, vals, context=context)
        
class unefa_horarios_seccion(osv.osv):

    _name='unefa.horarios_seccion'
    
    _columns = {
        'horario_id':fields.many2one('unefa.horarios','Horarios', required=False,ondelete='cascade', states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'seccion_id':fields.many2one('unefa.oferta_academica_seccion','Sección', required=True,states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'piso_id':fields.many2one('unefa.pisos','piso', required=True,states={'publicado': [('readonly', True)]}),
        'aula_id':fields.many2one('unefa.aulas','Aula', required=True,states={'publicado': [('readonly', True)]}),
        'datos_ids':fields.one2many('unefa.horarios_seccion_datos','secciones_horario_id','Datos', required=False,),
        'state':fields.selection([('aprobado','Aprobado'),('publicado','Publicado')],'Estado', required=False,),
        'creado':fields.boolean('Creado',),
        }
    
    def domain_seccion(self,cr,uid,ids,carrera_id,turno,pensum_id,periodo_id,context=None):
        oferta_obj=self.pool.get('unefa.oferta_academica')
        oferta_ids=oferta_obj.search(cr,uid,[('carrera_id','=',carrera_id),('turno','=',turno),('periodo_id','=',periodo_id)])
        list_secciones=[]
        list_aulas=[]
        oferta_data=oferta_obj.browse(cr,uid,oferta_ids)
        for o in oferta_data:
            for p in o.pensum_ids:
                if p.pensum_id.id==pensum_id:
                    for s in p.semestres_ids:
                        for sec in s.secciones_ids:
                            list_secciones.append(sec.id)
        user_obj=self.pool.get('res.users')
        user_ids=user_obj.search(cr,uid,[('id','=',uid)])
        user_data=user_obj.browse(cr,uid,user_ids)
        piso_id=user_data['coordinacion_id'].coordinaciones_ids.id
        
        dominio={'seccion_id': [('id', '=', list(list_secciones))]}
        val={'create_uid':uid,'piso_id':piso_id}
        return {'value':val,'domain':dominio,}
    
    def crear_horario(self,cr,uid,ids,context=None):
        url='/horarios/crear/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
            
    def editar_horario(self,cr,uid,ids,context=None):
        url='/horarios/editar/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
            
    def consultar_horario(self,cr,uid,ids,context=None):
        url='/horarios/consultar/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def descargar_horarios_particular(self,cr,uid,ids,context=None):
        url='/descargar/horarios_particular/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'aprobado',
            })
        return super(unefa_horarios_seccion,self).create(cr,uid,vals,context=context)
    
    
    def write(self, cr, uid, ids, vals, context=None):
        
        return super(unefa_horarios_seccion, self).write(cr, uid, ids, vals, context=context)
            
            
class unefa_horarios_seccion_datos(osv.osv):

    _name='unefa.horarios_seccion_datos'
    
    _columns = {
        'secciones_horario_id':fields.many2one('unefa.horarios_seccion','Horario',ondelete='cascade', required=False,),
        'dia_id':fields.many2one('unefa.horario_dias','Días', required=False,),
        'asignatura_id':fields.many2one('unefa.asignatura','Asignatura', required=False,),
        'hora_id':fields.many2one('unefa.horarios_horas','Hora', required=False,),
        }
    def write(self, cr, uid, ids, vals, context=None):
        
        
        
        return super(unefa_horarios_seccion_datos, self).write(cr, uid, ids, vals, context=context)
    
    


            
class unefa_horarios_horas(osv.osv):

    _name='unefa.horarios_horas'
    _rec_name='hora_completo'
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        for records in self.browse(cr, uid, ids):
            res.append((records.id, str(records.horas_desde) + ' ' + str(records.periodo_desde) + ' - ' + str(records.horas_hasta) + ' ' + str(records.periodo_hasta)))
        return res
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)
    
    
    _columns = {
        'horas_desde':fields.char('Hora Desde', required=True,),
        'horas_hasta':fields.char('Hora Hasta', required=True,),
        'periodo_desde':fields.selection([('AM','AM'),('PM','PM'),],'Período', required=True,),
        'periodo_hasta':fields.selection([('AM','AM'),('PM','PM'),],'Período', required=True,),
        'hora_completo':fields.function(_name_get_fnc, 'Horas Completo',type="char",),
        'active':fields.boolean('Activo')
        }
        
    _defaults={
        'active':True,
        }
    
    _sql_constraints = [
        ('horas_uniq', 'unique(horas_desde,horas_hasta,periodo_desde,periodo_hasta)', 'Ya existe un registro con estas horas.')
        ]
    
class unefa_horas_turno(osv.osv):

    _name='unefa.horas_turno'
    _rec_name='turno'
    
    _columns = {
        'periodo_id':fields.many2one('unefa.conf.periodo_academico','Período Académico', required=True, states={'aprobado': [('readonly', True)]}),
        'state':fields.selection([('borrador','BORRADOR'),('aprobado','APROBADO'),],'Estado', required=False, ),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO'),('sabatino','SABATINO')],'Turno', required=True, states={'aprobado': [('readonly', True)]}),
        'horas_ids':fields.many2many('unefa.horarios_horas','unefa_rel_horas_turno','turno_id','hora_id', states={'aprobado': [('readonly', True)]}),
        }
        
    _defaults={
        'active':True,
        'state':'borrador',
        }
        
    _sql_constraints = [
        ('horas_uniq', 'unique(turno,periodo_id)', 'Ya existe un registro para este turno y este período académico.')
        ]
    
    def aprobar_horas(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'aprobado'})
        
class unefa_horario_dias(osv.osv):

    _name='unefa.horario_dias'
    _rec_name='dia'
    
    _columns = {
        'dia':fields.char('Día', required=True,),
        }
    
    _sql_constraints = [
        ('dia_uniq', 'unique(dia)', 'Ya existe un registro con este día.')
        ]
    
    
