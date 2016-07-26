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

class unefa_grado_militar(osv.osv):

    _name='unefa.grado_militar'
    _rec_name='grado'
    
    _columns = {
        'grado':fields.char('Grado', required=True,),
        'fuerza_id': fields.many2many(
                            'unefa.fuerza_militar', 
                            'unefa_fuerza_grado_rel',
                            'grado_id',
                            'fuerza_id',
                            'Componente Militar',
                            required=True, 
                            help='Grado Militar'),
        'active':fields.boolean('Activo'),
        }
    _defaults={
        'active':True,
        }
        
    _order = 'create_date desc, id desc'
    
    _sql_constraints = [
        ('grado_uniq', 'unique(grado)', 'El Grado Militar que ingresó ya ha sido registrado.')
        ]
    
    def create(self, cr, uid, vals, context=None):
        vals.update({
            'grado':vals['grado'].upper(),
            })
        return super(unefa_grado_militar, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'grado' in vals.keys():
            vals.update({'grado':vals['grado'].upper(),})
        return super(unefa_grado_militar, self).write(cr, uid, ids, vals, context=context)
        
class unefa_fuerza_militar(osv.osv):

    _name='unefa.fuerza_militar'
    _rec_name='fuerza'
    
    _columns = {
        'fuerza':fields.char('Fuerza', required=True,),
        'active':fields.boolean('Activo'),
        }    
    _defaults={
        'active':True,
        }
    
    _order = 'create_date desc, id desc'
    
    _sql_constraints = [
        ('fuerza_uniq', 'unique(fuerza)', 'La Fuerza Militar que ingresó ya ha sido registrado.')
        ]

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'fuerza':vals['fuerza'].upper(),
            })
        return super(unefa_fuerza_militar, self).create(cr, uid, vals, context=context)
        
    def write(self, cr, uid, ids, vals, context=None):
        if 'fuerza' in vals.keys():
            vals.update({'fuerza':vals['fuerza'].upper(),})
        return super(unefa_fuerza_militar, self).write(cr, uid, ids, vals, context=context)
