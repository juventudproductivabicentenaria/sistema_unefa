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
#
from openerp.osv import fields, osv
from dateutil.relativedelta import * 
from datetime import datetime, date, time, timedelta
import time

class unefa_conf_periodo_academico(osv.osv):
    _name = 'unefa.conf.periodo_academico'
    _rec_name='periodo_academico'
    
    def periodo_activo(self, cr, uid, ids, context=None):
        periodo_obj=self.pool.get('unefa.conf.periodo_academico')
        periodo_ids=periodo_obj.search(cr,uid,[('state','=','activo')],context=context)
        return periodo_ids[0]
    
    _columns = {
        'periodo_academico': fields.char('Período académico', required=True,size=6),
        'fecha_inicio':fields.date(
                    'Fecha de Inicio',
                    readonly=False,
                    required=True,
                    help='Aquí se coloca la fecha de inicio del período académico'),
        'fecha_fin':fields.date(
                    'Fecha Final',
                    readonly=False,
                    required=True,
                    help='Aquí se coloca la fecha de final del período académico'),
        'state': fields.selection([
            ('inactivo', 'Inactivo'),
            ('activo', 'Activo'),
            ], 'Estado', readonly=True, copy=False, help="Este es es estado actual del período académico.", select=True),
    }
    
    _defaults = {
        'state': 'inactivo',
    }
    
    _sql_constraints = [
        ('periodo_academico_unico', 'unique (periodo_academico)', 'El período académico ya existe')
    ]
    
    _order = 'create_date desc, id desc'

    def activar_periodo(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state':'activo'},context=context)
        
    def desactivar_periodo(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'},context=context)
    
    def validar_fecha_periodo(self, cr, uid, ids,fecha_inicio,fecha_fin, context=None):
        mensaje={}
        fechas = {}
        if fecha_inicio and fecha_fin:
            if cmp(fecha_fin, fecha_inicio) == -1 or cmp(fecha_fin, fecha_inicio) == 0:
                    mensaje={
                        'title':('Error de fecha'),
                        'message':('La fecha final no puede ser menor\
                                    o igual a la fecha de inicio.'),
                        }
                    fechas={
                        'fecha_inicio':'',
                        'fecha_fin':'',
                        }
            
        return {
            'warning':mensaje,
            'value':fechas
                }

class cronograma_actividades(osv.osv):
    _name = 'unefa.cronograma_actividades'
    
    _rec_name = "actividad"
    
    _columns = {
        'actividad':fields.char('Actividad', required=True,),
        'activo':fields.boolean('Actividad Activa',)
    
    }
    
    _defaults={
        'activo':True,
        }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'actividad':vals['actividad'].upper(),
            })
        return super(cronograma_actividades, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'actividad' in vals.keys():
            vals.update({'actividad':vals['actividad'].upper(),})
        return super(cronograma_actividades, self).write(cr, uid, ids, vals, context=context)
