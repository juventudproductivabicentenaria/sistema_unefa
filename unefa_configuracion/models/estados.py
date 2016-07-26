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

class unefa_estados(osv.osv):
    _name='unefa.estados'
    _description='Registro de los Estados'
    _rec_name='estado'
    
    _columns={
        'estado': fields.char(
                            'Estado', 
                            size=50, 
                            required=True, 
                            help='Nombre  del  Estado'),
        'codigo': fields.char(
                            'Código', 
                            size=10, 
                            required=True, 
                            help='Código  de  Identificación del Estado'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'redi_id': fields.many2one(
                            'unefa.redi', 
                            'REDI',
                            required=True, 
                            help='Redi que está asociado al Estado'),
    }
    
    _defaults = {
        'active':True, 
    }
    
    _sql_constraints = [
        ('codigo_uniq', 'unique(codigo)', 'El Código que ingresó ya ha sido registrado.')
        ]
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'estado':vals['estado'].upper(),
            'codigo':vals['codigo'].upper(),
            })
        return super(unefa_estados, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'estado' in vals.keys():
            vals.update({'estado':vals['estado'].upper(),})
        if 'codigo' in vals.keys():
            vals.update({'codigo':vals['codigo'].upper(),})
        return super(unefa_estados, self).write(cr, uid, ids, vals, context=context)

