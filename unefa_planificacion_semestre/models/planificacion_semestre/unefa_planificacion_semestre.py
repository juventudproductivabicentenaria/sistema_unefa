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
from openerp import http,tools, api,SUPERUSER_ID
import sys
reload(sys)
sys.setdefaultencoding('UTF8')


class unefa_planificacion_semestre(osv.osv):
    _name = 'unefa.planificacion_semestre'
    _rec_name = 'nombre'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
   
    def default_carrera(self, cr, uid, ids, context=None):
        users_obj=self.pool.get('res.users')
        users_ids=users_obj.search(cr,uid,[('id','=',uid)],context=context)
        users_data=users_obj.browse(cr,uid,users_ids)
        return int(users_data['carrera_id'])
            
    _columns = {
        'nombre': fields.char('Nombre de planificación', required=True,size=80),
        'carrera_id': fields.many2one(
                                'unefa.carrera',
                                'Carrera',
                                required=False,
                                readonly=True,
                                ),
        'periodo_id': fields.many2one(
                                'unefa.conf.periodo_academico',
                                'Período Académico',
                                required=True,
                                readonly=False,
                                states={'borrador': [('readonly', False)]},
                                ),
        'observaciones': fields.text(
                                'Observaciones'
                                ),
        'actividad_ids': fields.one2many(
                                    'unefa.cronograma', 
                                    'planif_id', 
                                    'Actividad',
                                    required=True),
        'state': fields.selection([
                            ('borrador', 'Borrador'),
                            ('aprobado', 'Aprobado'),], 
                            'Estatus', 
                            readonly=True, 
                            help="Este es es estado actual del cronograma.",
                            ),
        'turno': fields.selection([
                            ('nocturno', 'NOCTURNO'),
                            ('diurno', 'DIURNO'),], 
                            'Turno', 
                            required=True, 
                            help="Este es es estado actual del cronograma.",
                            ),
        'cronograma_ids': fields.many2many('ir.attachment', 'cronograma_attachment_rel', 'cronograma_id', 'attachment_id', 'Descargar Cronograma'),
    }
    
    _defaults = {
        'carrera_id': default_carrera,
        'create_date': fields.datetime.now,
    }
    
    _order = 'create_date desc, id desc'
    
    def onchange_peridodo_id(self, cr, uid, ids,context=None):
        list_periodo=[]
        domain={}
        planifiacion_id=self.search(cr,uid,[],context=context)
        for i in self.browse(cr,uid,planifiacion_id):
            list_periodo.append(i.periodo_id)
        periodo_obj=self.pool.get('unefa.conf.periodo_academico')
        for n in list_periodo:
            periodo_ids=periodo_obj.search(cr,uid,[('id','!=',int(n))],context=context)
            domain = {'periodo_id': [('id', '=', list(periodo_ids))]}
        return {'domain': domain}
    
    def onchange_cronograma(self, cr, uid, ids, context=None):
        res={}
        cronograma_obj=self.pool.get('unefa.cronograma_actividades')
        cronograma_ids=cronograma_obj.search(cr,uid,[('activo','=','True')],context=context)
        cronograma_datos=cronograma_obj.browse(cr,uid,cronograma_ids,context=context)
        list_actividad=[]
        for i in cronograma_datos:
            list_actividad.append([0,False,{'actividad_id':i.id }])
        res={
            'actividad_ids':list_actividad,
            }
        return {'value':res}
    
    def aprobar_planificacion(self, cr, uid, ids, context=None):
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
            'body': 'Ha sido aprobada la planificación semestral para el período '+periodo+'.', 
            'model': 'unefa.planificacion_semestre', 
            'res_id': ids[0], 
            'parent_id': False, 
            'subtype_id': False, 
            'author_id': uid, 
            'type': 'notification', 
            'notified_partner_ids': [[6, False, list_partners]], 
            'subject': False}
            
        mail_message_obj.create(cr,SUPERUSER_ID,values)
        
        return self.write(cr, uid, ids, {'state':'aprobado'})
        
    def create(self,cr,uid,vals,context=None):
        vals.update({
            'state':'borrador',
            })
        ids=self.search(cr,uid,[('periodo_id','=',vals['periodo_id'])])
        if len(ids)==1:
            peridodo_obj=self.pool.get('unefa.conf.periodo_academico')
            periodo_ids=peridodo_obj.search(cr,uid,[('id','=',vals['periodo_id'])],context=context)
            periodo_datos=peridodo_obj.browse(cr,uid,periodo_ids,context=context)
            raise osv.except_osv(('Error !'), ('Ya existe un Cronograma Académico con el periodo '+periodo_datos['periodo_academico'].upper()+' no esta asignado al parque.'))
        return super(unefa_planificacion_semestre,self).create(cr,uid,vals,context=context)
    
    
class cronograma(osv.osv):
    _name = 'unefa.cronograma'

    
    _columns = {
        'planif_id': fields.many2one(
                                'unefa.planificacion_semestre',
                                'Actividad'
                                ),
        'actividad_id': fields.many2one(
                                    'unefa.cronograma_actividades',
                                    'Actividad',
                                    readonly=True,
                                    ),
        'fecha_desde': fields.date(
                                    'Fecha Inicio',
                                    required=True,
                                    ),
        'fecha_hasta': fields.date(
                                    'Fecha Final',
                                    required=True,
                                    ),
        'cronograma_ids': fields.many2many('ir.attachment', 'cronograma_attachment_rel', 'cronograma_id', 'attachment_id', 'Descargar Cronograma'),
    }
    
    
        
    
    def onchange_fecha(self, cr, uid, ids, fecha_desde, fecha_hasta, periodo_id, context=None):
        res={}
        warning={}
        periodo_obj=self.pool.get('unefa.conf.periodo_academico')
        periodo_ids=periodo_obj.search(cr,uid,[('id','=',int(periodo_id))],context=context)
        periodo_data=periodo_obj.browse(cr,uid,periodo_ids,context=context)
        for fecha in periodo_data:
            fecha_ini_periodo = fecha.fecha_inicio
            fecha_fin_periodo = fecha.fecha_fin
        if fecha_desde:
            if cmp(fecha_desde,fecha_hasta)==1:
                res={
                    'fecha_hasta':'',
                    }
                warning={
                    'title':('Error de fechas'),
                    'message':('La fecha de inicio no puede ser mayo a la fecha final'),
                    }
            if cmp(fecha_hasta, fecha_ini_periodo) == -1 or cmp(fecha_hasta, fecha_fin_periodo) == 1:
                warning={
                        'title':('Error'),
                        'message':('La fecha para la actividad no puede \
                                    ser menor a la fecha de inicio, ni \
                                    mayor a la fecha final del período académico.'),
                        }
                res={
                    'fecha_hasta':'',
                    } 
        else:
            res={
                'fecha_hasta':'',
                }
            warning={
                    'title':('Error'),
                    'message':('Debe seleccionar una fecha de inicio'),
                    }
        
        return {'warning':warning,'value':res}
                
    def validar_fecha_cronograma(self, cr, uid, ids, fecha_desde,periodo_id, context=None):
        warning={}
        value={}
        if not periodo_id:            
            warning={
                        'title':('Aviso!'),
                        'message':('Debe seleccionar el período académico'),
                        }
            value={
                'fecha_desde':''
                }
            return {'warning':warning,'value':value}
        
        periodo_obj=self.pool.get('unefa.conf.periodo_academico')
        periodo_ids=periodo_obj.search(cr,uid,[('id','=',int(periodo_id))],context=context)
        periodo_data=periodo_obj.browse(cr,uid,periodo_ids,context=context)
        for fecha in periodo_data:
            fecha_ini_periodo = fecha.fecha_inicio
            fecha_fin_periodo = fecha.fecha_fin
        if cmp(fecha_desde, fecha_ini_periodo) == -1 or cmp(fecha_desde, fecha_fin_periodo) == 1:
            warning={
                    'title':('Error'),
                    'message':('La fecha para la actividad no puede ser menor a la fecha de inicio, ni mayor a la fecha final del período académico.'),
                    }
            value={
                'fecha_desde':''
                }
        return {'warning':warning,'value':value}
