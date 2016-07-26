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

class unefa_cronograma_recuperacion(osv.osv):

    _name='unefa.cronogramas_recuperacion'
    _rec_name="id"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    
    _columns = {
        'carrera_id':fields.many2one('unefa.carrera','Carrera', required=True,readonly=True,),
        'turno':fields.selection([('nocturno','NOCTURNO'),('diurno','DIURNO'),],'Turno', required=True,readonly=True),
        'state':fields.selection([('borrador','Borrador'),('aprobado','Aprobado'),('publicado','Publicado')],'Estado', required=False,),
        'periodo_id':fields.many2one('unefa.conf.periodo_academico','Período Académico', required=True, readonly=True),
        'pensum_ids':fields.one2many('unefa.cronograma_recuperacion_pensum','recuperacion_id','Pensums', required=True,),
        'fecha_inicio':fields.date('Fecha Inicio', required=False, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'fecha_fin':fields.date('Fecha Inicio', required=False, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        }
    
    _sql_constraints = [
        ('horario_uniq', 'unique(carrera_id,turno,periodo_id)', 'Ya existe un registro para este Período Académico.')
        ]
            
            
    def aprobar_cronograma_recuperacion(self,cr,uid,ids,context=None):
        cronograma_recuperacion_obj=self.pool.get('unefa.cronograma_recuperacion_line')
        cronograma_recuperacion_pensum_obj=self.pool.get('unefa.cronograma_recuperacion_pensum')
        cronograma_recuperacion_pensum_ids=cronograma_recuperacion_pensum_obj.search(cr,uid,[('recuperacion_id','=',ids[0])])
        for ids_cron in cronograma_recuperacion_pensum_ids:
            cronograma_recuperacion_pensum_obj.write(cr,uid,ids_cron,{'state':'aprobado'})
            cronograma_recuperacion_ids=cronograma_recuperacion_obj.search(cr,uid,[('cronograma_line_id','=',ids_cron)])
            for ids_c in cronograma_recuperacion_ids:
                cronograma_recuperacion_obj.write(cr,uid,ids_c,{'state':'aprobado'})
        return self.write(cr,uid,ids,{'state':'aprobado'})
    
    def publicar_cronograma_recuperacion(self,cr,uid,ids,context=None):
        cronograma_recuperacion_obj=self.pool.get('unefa.cronograma_recuperacion_line')
        cronograma_recuperacion_pensum_obj=self.pool.get('unefa.cronograma_recuperacion_pensum')
        cronograma_recuperacion_pensum_ids=cronograma_recuperacion_pensum_obj.search(cr,uid,[('recuperacion_id','=',ids[0])])
        for ids_cron in cronograma_recuperacion_pensum_ids:
            cronograma_recuperacion_pensum_obj.write(cr,uid,ids_cron,{'state':'publicado'})
            cronograma_recuperacion_ids=cronograma_recuperacion_obj.search(cr,uid,[('cronograma_line_id','=',ids_cron)])
            for ids_c in cronograma_recuperacion_ids:
                cronograma_recuperacion_obj.write(cr,uid,ids_c,{'state':'publicado'})
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
            'body': 'Ha sido aprobado el cronograma de recuperación para el período '+periodo+'.', 
            'model': 'unefa.cronogramas_recuperacion', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, list_partners]], 
            'subject': False}
            
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        return self.write(cr,uid,ids,{'state':'publicado'})
        
    def descargar_cronograma_recuperacion(self,cr,uid,ids,context=None):
        url='/cronograma_recuperacion/descargar/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }    
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_cronograma_recuperacion,self).create(cr,uid,vals,context=context)
        
class unefa_cronograma_recuperacion_pensum(osv.osv):

    _name='unefa.cronograma_recuperacion_pensum'
    
    _columns = {
        'recuperacion_id':fields.many2one('unefa.cronograma_recuperacion','Cronograma Reparación', required=False,ondelete='cascade', states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'pensum_id':fields.many2one('unefa.pensum','Pensum', required=False, readonly=True),
        'state':fields.selection([('borrador','Borrador'),('aprobado','Aprobado'),('publicado','Publicado')],'Estado', required=False,),
        'cronograma_line_ids':fields.one2many('unefa.cronograma_recuperacion_line','cronograma_line_id','Cronograma', required=True,),
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_cronograma_recuperacion_pensum,self).create(cr,uid,vals,context=context)
        
class unefa_cronograma_recuperacion_line(osv.osv):

    _name='unefa.cronograma_recuperacion_line'
    
    _columns = {
        'cronograma_line_id':fields.many2one('unefa.cronograma_recuperacion_pensum','Pensum Cronograma', required=False,ondelete='cascade'),
        'state':fields.selection([('borrador','Borrador'),('aprobado','Aprobado'),('publicado','Publicado')],'Estado', required=False,),
        'semestre_id':fields.many2one('unefa.semestre','Semestre', required=False, readonly=True),
        'seccion_id':fields.many2one('unefa.oferta_academica_seccion','Sección', required=False, readonly=True),
        'asignatura_id':fields.many2one('unefa.asignatura','Asignatura', required=False, readonly=True),
        'profesor_id':fields.many2one('res.users','Profesor', required=False, readonly=True),
        'fecha_recuperacion':fields.date('Fecha',required=False, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'hora':fields.char('Hora', required=False, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'horario':fields.selection([('AM','AM'),('PM','PM')],'Período', required=False, states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        'observaciones':fields.text('Observaciones', states={'aprobado': [('readonly', True)],'publicado': [('readonly', True)]}),
        }
        
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'state':'borrador',
            })
        return super(unefa_cronograma_recuperacion_line,self).create(cr,uid,vals,context=context)
    
    
