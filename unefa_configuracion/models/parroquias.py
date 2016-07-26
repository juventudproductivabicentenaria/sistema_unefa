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

class unefa_parroquias(osv.osv):
    _name='unefa.parroquias'
    _description='Registro de Parroquia'
    _rec_name='parroquia'
    
    _columns = {
        'parroquia': fields.char(
                            'Parroquia', 
                            size=100, 
                            required=True, 
                            help='Nombre  de la Parroquia'),
        'codigo': fields.char(
                            'Código', 
                            size=10, 
                            required=True, 
                            help='Código de Identificación de la Parroquia'),
        'active': fields.boolean(
                            'Activo',
                            help='Estatus del registro Activado-Desactivado'),
        'municipio_id': fields.many2one(
                            'unefa.municipios', 
                            'Municipio', 
                            required=True,
                            help='Municipio que  está \
                            asociado  a la  Parroquia'),
        }
    
    _defaults = {
        'active':True, 
    }
    
    _sql_constraints = [
        ('codigo_uniq', 'unique(codigo)', 'La Código que ingresó ya ha sido registrado.')
        ]
    
    def cp_limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'parroquia':vals['parroquia'].upper(),
            'codigo':vals['codigo'].upper(),
            })
        return super(unefa_parroquias, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'parroquia' in vals.keys():
            vals.update({'parroquia':vals['parroquia'].upper(),})
        if 'codigo' in vals.keys():
            vals.update({'codigo':vals['codigo'].upper(),})
        return super(unefa_parroquias, self).write(cr, uid, ids, vals, context=context)

