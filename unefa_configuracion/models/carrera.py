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

class unefa_carrera(osv.osv):
    _name='unefa.carrera'
    _rec_name='nombre'
    
    _columns={
        'nombre':fields.char('Nombre',
                            size=80,
                            required=True,
                            states={'activo': [('readonly', True)]},
                            help='Aquí se coloca el nombre de la Carrera'),
        'area_conocimiento_id': fields.many2one(
                            'unefa.area_conocimiento', 
                            'Área de conocimiento',
                            required=True, 
                            help='Área de conocimiento de la carrera'),
        'codigo':fields.char('Codigo', required=True,
                            states={'activo': [('readonly', True)]},
                            help='Aquí se coloca el codigo de la carrera'),
        'nucleo_ids':fields.many2many('unefa.nucleo',
                                    'unefa_nucleo_carrera_rel',
                                    'carrera_id','nucleo_id',
                                    'Sede'),
        'tipo':fields.selection([('corta','Carrera Corta'),
                                ('larga','Carrera Larga')],'Tipo',
                                required=True, states={'activo': [('readonly', True)]},
                                help='Carrera Larga o Corta'),
        'active':fields.boolean('Activo',
                                help='Si esta activo el motor lo incluira en la vista...'),
        'state':fields.selection([('inactivo','Inactivo'),('activo','Activo')],
                                'Estatus', required=False,
                                help='Estatus de la Carrera'),
        }
    
    _defaults={
        'active':True,
        }

    _order = 'create_date desc, id desc'
    
    _sql_constraints = [
        ('nombre_uniq', 'unique(nombre)', 'La carrera que ingresó ya ha sido registrada.'),
        ('codigo_uniq', 'unique(codigo)', 'El código que ingresó ya ha sido registrada.')
        ]
    
    def activar_carrera(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'activo'})
    
    def desactivar_carrera(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'inactivo'})
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'nombre':vals['nombre'].upper(),
            'codigo':vals['codigo'].upper(),
            #~ 'state':'inactivo',
            })
        return super(unefa_carrera, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'codigo' in vals.keys():
            vals.update({'codigo':vals['codigo'].upper(),})
        return super(unefa_carrera, self).write(cr, uid, ids, vals, context=context)

class unefa_area_conocimiento(osv.osv):
    _name='unefa.area_conocimiento'
    _rec_name='area_conocimiento'
    
    _columns={
        'area_conocimiento':fields.char('Área de conocimiento',
                                        size=80,
                                        required=True,
                                        help='Aquí se coloca el nombre del área de conocimiento'),
        'active':fields.boolean('Activo',
                                help='Si esta activo el motor lo incluira en la vista del registro...'),
        
        }
    
    _defaults={
        'active':True,
        }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'area_conocimiento':vals['area_conocimiento'].upper(),
            })
        return super(unefa_area_conocimiento, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'area_conocimiento' in vals.keys():
            vals.update({'area_conocimiento':vals['area_conocimiento'].upper(),})
        return super(unefa_area_conocimiento, self).write(cr, uid, ids, vals, context=context)
