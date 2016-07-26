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

class unefa_region_defensa_integral(osv.osv):
    _name='unefa.region_defensa_integral'
    _description='Registro de la Region de Defensa Integral'
    _rec_name='region_defensa_integral'
    
    _columns={
        'region_defensa_integral': fields.char(
                            'Región de Defensa Integral', 
                            size=50, 
                            required=True, 
                            help='Nombre  de la región de Defensa Integral'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'estados_ids': fields.many2many(
                            'unefa.estados', 
                            'rel_region_estado',
                            'region_id',
                            'estado_id', 
                            'Estados',
                            required=True, 
                            help='Estados asociados a la región de defensa integral'),
    }
    
    _defaults = {
        'active':True, 
    }
    
    _sql_constraints = [
        ('codigo_uniq', 'unique(region_defensa_integral)', 'La región ingresada ya existe.')
        ]
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'region_defensa_integral':vals['region_defensa_integral'].upper(),
            })
        return super(unefa_region_defensa_integral, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'region_defensa_integral' in vals.keys():
            vals.update({'region_defensa_integral':vals['estado'].upper(),})
        return super(unefa_region_defensa_integral, self).write(cr, uid, ids, vals, context=context)

