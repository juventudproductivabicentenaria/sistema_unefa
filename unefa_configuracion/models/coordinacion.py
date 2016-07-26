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

import time
from openerp.osv import fields, osv

class unefa_coordinacion(osv.osv):
    _name='unefa.coordinacion'
    _rec_name='nombre'
    
    _columns={
        'nombre':fields.char('Nombre',
                            size=80,
                            required=True,
                            states={'activo': [('readonly', True)]},
                            help='Aquí se coloca el nombre de la Coordinación'),
        'regimen':fields.selection([('nocturno','NOCTURNO'),
                            ('diurno','DIURNO')],
                            'Turno', 
                            required=True,
                            states={'activo': [('readonly', True)]},),
        'carrera_id':fields.many2one('unefa.carrera',
                            'Carrera', 
                            required=True,
                            states={'activo': [('readonly', True)]},),
        'sede_id':fields.many2one('unefa.nucleo',
                            'Sede', 
                            required=True,
                            states={'activo': [('readonly', True)]},),
        'descripcion':fields.text('Descripción',
                            help='Aquí se coloca la descripcion de la coordinación'),
        'ubicacion':fields.char('Ubicación',
                            size=80,
                            help='Aquí se coloca la ubicación de la coordinación'),
        'telefono':fields.char('Teléfono',
                            size=20,
                            help='Aquí se coloca el telefono de la coordinación'),
        'email':fields.char('Email',
                            help='Aquí se coloca el Email de la coordinación'),
        'coordinaciones_ids': fields.many2many('unefa.pisos', 
                            'unefa_piso_coordinacion_rel', 
                            'coordinacion_id', 
                            'piso_id', 
                            'Piso'),
        'active':fields.boolean('Activo',
                            help='Si esta activo el motor lo incluira en la vista...'),
        'state':fields.selection([('inactivo','Inactivo'),
                            ('activo','Activo')],'Estatus', 
                            required=False, 
                            help='Estatus de la Coordinación'),
        }
    
    _defaults={
        'active':True,
        }
    
    _order = 'create_date desc, id desc'
        
    _sql_constraints = [
        ('nombre_uniq', 'unique(nombre)', 'La Coordinación que ingresó ya ha sido registrada.')
        ]
        
    def activar_coordinacion(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'activo'})
        
    def desactivar_coordinacion(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'})
    
    def crear_lista_general_coordinacion(self,cr,uid,ids,context=None):
        url='/descargar/listas_general_estudiantes/%d' %ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url':url,
            'target': 'new',
            }
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'nombre':vals['nombre'].upper(),
            #~ 'state':'inactivo',
            })
        return super(unefa_coordinacion, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'nombre' in vals.keys():
            vals.update({'nombre':vals['nombre'].upper(),})
        return super(unefa_coordinacion, self).write(cr, uid, ids, vals, context=context)
