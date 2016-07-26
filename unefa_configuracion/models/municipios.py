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

class unefa_municipios(osv.osv):
    _name='unefa.municipios'
    _rec_name='municipio'
    _description='Registro de Municipio'
    
    _columns = {
        'municipio': fields.char(
                            'Municipio', 
                            size=100, 
                            required=True, 
                            help='Nombre  de la Municipio'),
        'codigo': fields.char(
                            'Código', 
                            size=10, 
                            required=True, 
                            help='Código de Identificación de la Municipio'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'estado_id': fields.many2one(
                            'unefa.estados', 
                            'Estado',
                            required=True, 
                            help='Estado que está asociado al Municipio'),
        
    }
    
    _defaults = {
        'active':True, 
    }
        
    _sql_constraints = [
        ('codigo_uniq', 'unique(codigo)', 'El Código que ingresó ya ha sido registrado.')
        ]
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'municipio':vals['municipio'].upper(),
            'codigo':vals['codigo'].upper(),
            })
        return super(unefa_municipios, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'municipio' in vals.keys():
            vals.update({'municipio':vals['municipio'].upper(),})
        if 'codigo' in vals.keys():
            vals.update({'codigo':vals['codigo'].upper(),})
        return super(unefa_municipios, self).write(cr, uid, ids, vals, context=context)
